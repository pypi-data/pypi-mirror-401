use anyhow::Result;
use iroh::{Endpoint, SecretKey};
use iroh_tickets::endpoint::EndpointTicket;
use std::net::SocketAddr;
use tracing::info;

use crate::cli::{HivemindJoinArgs, JoinEvent, JoinEventData, Services, OutputFormat};
use crate::output::{self, events, status};
use crate::handlers::handle_peer_listener;
use crate::{PORT_ID_FRONTEND, PORT_ID_BACKEND, PORT_ID_WS};

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
    
    Ok(crate::HiveConfig::new(frontend_listen, backend_listen, ws_listen))
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
        frontend: config.frontend().to_string(),
        backend: config.backend().to_string(),
        websocket: config.websocket().to_string(),
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
    // Start three TCP listeners
    let frontend_listener = tokio::net::TcpListener::bind(config.frontend()).await?;
    let backend_listener = tokio::net::TcpListener::bind(config.backend()).await?;
    let ws_listener = tokio::net::TcpListener::bind(config.websocket()).await?;

    info!("TCP listeners started");

    // Spawn tasks for each listener
    let conn1 = connection.clone();
    let frontend_task = tokio::spawn(async move {
        handle_peer_listener(conn1, frontend_listener, PORT_ID_FRONTEND).await
    });

    let conn2 = connection.clone();
    let backend_task = tokio::spawn(async move {
        handle_peer_listener(conn2, backend_listener, PORT_ID_BACKEND).await
    });

    let conn3 = connection.clone();
    let ws_task = tokio::spawn(async move {
        handle_peer_listener(conn3, ws_listener, PORT_ID_WS).await
    });

    // Wait for all tasks (or until Ctrl+C)
    tokio::select! {
        _ = frontend_task => {},
        _ = backend_task => {},
        _ = ws_task => {},
        _ = tokio::signal::ctrl_c() => {
            eprintln!("Shutting down...");
        }
    }

    Ok(())
}