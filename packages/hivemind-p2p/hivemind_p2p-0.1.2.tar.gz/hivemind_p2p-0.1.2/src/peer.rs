use anyhow::Result;
use iroh::{Endpoint, SecretKey};
use iroh_tickets::endpoint::EndpointTicket;
use std::net::SocketAddr;
use tracing::info;

use crate::cli::{HivemindJoinArgs, JoinEvent, JoinEventData, Services, OutputFormat};
use crate::output::{self, events, status};
use crate::handlers::handle_peer_listener;

/// Handle the join (peer) command
pub async fn handle_join(args: HivemindJoinArgs) -> Result<()> {
    let use_json = args.common.output_format == OutputFormat::Json;

    output::log_info(&format!("Starting Hivemind P2P Peer: {}", args.name), use_json);

    validate_join_args(&args)?;

    let config = create_peer_config(&args)?;
    let ticket_str = get_ticket_string(&args, use_json).await?;
    let (_endpoint, connection, hub_id) = connect_to_hub(&args, &ticket_str, use_json).await?;

    let local_services = create_services_config(&config);
    display_connection_success(&args, &hub_id, &local_services, use_json);

    run_peer_services(connection, config).await
}

/// Validate that required arguments are provided
fn validate_join_args(args: &HivemindJoinArgs) -> Result<()> {
    if args.ticket.is_none() && args.join_code.is_none() {
        anyhow::bail!("Either --ticket or --join-code must be provided");
    }
    Ok(())
}

/// Create peer configuration from command line arguments
fn create_peer_config(args: &HivemindJoinArgs) -> Result<crate::HiveConfig> {
    let frontend_listen: SocketAddr = args.frontend_addr.parse()?;
    let backend_listen: SocketAddr = args.backend_addr.parse()?;
    let ws_listen: SocketAddr = args.ws_addr.parse()?;

    let services = vec![
        crate::Service {
            label: "frontend".to_string(),
            addr: frontend_listen,
        },
        crate::Service {
            label: "backend".to_string(),
            addr: backend_listen,
        },
        crate::Service {
            label: "websocket".to_string(),
            addr: ws_listen,
        },
    ];
    
    Ok(crate::HiveConfig::new(services))
}

/// Get ticket string either directly or via Magic Wormhole
async fn get_ticket_string(args: &HivemindJoinArgs, use_json: bool) -> Result<String> {
    if let Some(code) = &args.join_code {
        output::log_info(&format!("Connecting via Magic Wormhole with code: {}", code), use_json);
        
        if !use_json {
            output::display_box("Connecting via Magic Wormhole...");
            println!();
        }

        crate::wormhole::receive_ticket_via_wormhole(
            code,
            args.common.wormhole_relay.clone(),
        ).await
    } else {
        Ok(args.ticket.as_ref().unwrap().clone())
    }
}

/// Connect to the hub using the ticket
async fn connect_to_hub(
    args: &HivemindJoinArgs,
    ticket_str: &str,
    use_json: bool,
) -> Result<(Endpoint, iroh::endpoint::Connection, String)> {
    output::log_info("Received ticket, parsing...", use_json);

    // Parse ticket
    let ticket: EndpointTicket = ticket_str.parse()
        .map_err(|e| anyhow::anyhow!("Failed to parse ticket: {}", e))?;
    let endpoint_addr = ticket.endpoint_addr().clone();
    let hub_id = endpoint_addr.id.to_string();

    // Generate secret key for this peer
    let secret_key = SecretKey::generate(&mut rand::rng());

    // Create endpoint
    let endpoint = Endpoint::builder()
        .secret_key(secret_key)
        .alpns(vec![args.common.alpn.as_bytes().to_vec()])
        .bind()
        .await?;

    output::log_info(&format!("Connecting to hub: {}", hub_id), use_json);

    // Connect to the hub
    let connection = endpoint.connect(endpoint_addr, args.common.alpn.as_bytes()).await?;

    eprintln!("Connected to hub!");
    
    Ok((endpoint, connection, hub_id))
}

/// Create services configuration object
fn create_services_config(config: &crate::HiveConfig) -> Services {
    Services {
        services: config.services.iter().cloned().collect(),
    }
}

/// Display successful connection information
fn display_connection_success(
    args: &HivemindJoinArgs,
    hub_id: &str,
    local_services: &Services,
    use_json: bool,
) {
    if use_json {
        let event = JoinEvent {
            event_type: events::PEER_CONNECTED.to_string(),
            timestamp: output::get_current_timestamp(),
            data: JoinEventData {
                peer_name: args.name.clone(),
                hub_id: Some(hub_id.to_string()),
                local_services: local_services.clone(),
                status: status::CONNECTED.to_string(),
            },
        };
        output::output_json(&event);
    }

    output::display_peer_startup(&args.name, use_json, local_services);
}

/// Start the peer services (TCP listeners)
async fn run_peer_services(
    connection: iroh::endpoint::Connection,
    config: crate::HiveConfig,
) -> Result<()> {
    // Start TCP listeners for all configured services
    let mut listeners = Vec::new();
    
    for (port_id, service) in config.services.iter().enumerate() {
        let listener = tokio::net::TcpListener::bind(service.addr).await?;
        listeners.push((listener, port_id as u8, service.label.clone()));
    }

    info!("TCP listeners started for {} services", listeners.len());

    // Spawn tasks for each listener
    let mut tasks = Vec::new();
    
    for (listener, port_id, service_label) in listeners {
        let conn = connection.clone();
        let config_clone = config.clone();
        let task = tokio::spawn(async move {
            info!("Starting listener for service '{}' (port_id: {})", service_label, port_id);
            handle_peer_listener(conn, listener, port_id, &config_clone).await
        });
        tasks.push(task);
    }

    // Wait for all tasks (or until Ctrl+C)
    let mut select_branches = Vec::new();
    for task in tasks {
        select_branches.push(task);
    }
    
    tokio::select! {
        result = async {
            // Wait for the first task to complete
            for task in select_branches {
                if let Err(e) = task.await {
                    eprintln!("Task failed: {}", e);
                }
            }
        } => { result },
        _ = tokio::signal::ctrl_c() => {
            eprintln!("Shutting down...");
        }
    }

    Ok(())
}