use anyhow::Result;
use iroh::{Endpoint, SecretKey};
use iroh_tickets::endpoint::EndpointTicket;
use std::net::SocketAddr;
use tracing::{info, warn, error};

use crate::cli::{HivemindShareArgs, ShareEvent, ShareEventData, Services, OutputFormat};
use crate::output::{self, events, status};
use crate::handlers::handle_hub_connection;

/// Handle the share (hub) command
pub async fn handle_share(args: HivemindShareArgs) -> Result<()> {
    let use_json = args.common.output_format == OutputFormat::Json;
    
    output::log_info(&format!("Starting Hivemind P2P Hub: {}", args.name), use_json);

    let config = create_hub_config(&args)?;
    let endpoint = create_hub_endpoint(&args).await?;
    let (ticket_str, node_id, services) = create_hub_ticket(&endpoint, &config);

    if args.wormhole {
        handle_wormhole_mode(&args, &ticket_str, &node_id, &services, use_json).await?;
    } else {
        handle_direct_mode(&args, &ticket_str, &node_id, &services, use_json);
    }

    run_hub_loop(endpoint, config).await
}

/// Create configuration from command line arguments
fn create_hub_config(args: &HivemindShareArgs) -> Result<crate::HiveConfig> {
    let frontend_addr: SocketAddr = args.frontend_addr.parse()?;
    let backend_addr: SocketAddr = args.backend_addr.parse()?;
    let ws_addr: SocketAddr = args.ws_addr.parse()?;
    
    Ok(crate::HiveConfig::new(frontend_addr, backend_addr, ws_addr))
}

/// Create and configure the hub endpoint
async fn create_hub_endpoint(args: &HivemindShareArgs) -> Result<Endpoint> {
    let secret_key = SecretKey::generate(&mut rand::rng());

    let mut endpoint_builder = Endpoint::builder()
        .secret_key(secret_key)
        .alpns(vec![args.common.alpn.as_bytes().to_vec()]);

    // Add bind addresses if specified
    if let Some(v4) = args.common.ipv4_addr {
        endpoint_builder = endpoint_builder.bind_addr_v4(v4);
    }
    if let Some(v6) = args.common.ipv6_addr {
        endpoint_builder = endpoint_builder.bind_addr_v6(v6);
    }

    Ok(endpoint_builder.bind().await?)
}

/// Create the endpoint ticket and extract relevant information
fn create_hub_ticket(
    endpoint: &Endpoint, 
    config: &crate::HiveConfig
) -> (String, String, Services) {
    let endpoint_addr = endpoint.addr();
    let node_id = endpoint_addr.id.to_string();
    let ticket = EndpointTicket::new(endpoint_addr);
    let ticket_str = ticket.to_string();

    let services = Services {
        frontend: config.frontend().to_string(),
        backend: config.backend().to_string(),
        websocket: config.websocket().to_string(),
    };

    (ticket_str, node_id, services)
}

/// Handle Magic Wormhole mode
async fn handle_wormhole_mode(
    args: &HivemindShareArgs,
    ticket_str: &str,
    node_id: &str,
    services: &Services,
    use_json: bool,
) -> Result<()> {
    output::display_hub_startup(&args.name, use_json, true, None);

    if use_json {
        output::log_info(&format!("Node ID: {}", node_id), true);
        
        let event = ShareEvent {
            event_type: events::HUB_READY.to_string(),
            timestamp: output::get_current_timestamp(),
            data: ShareEventData {
                hub_name: args.name.clone(),
                ticket: Some(ticket_str.to_string()),
                join_code: None,
                node_id: node_id.to_string(),
                services: services.clone(),
                status: status::WORMHOLE_MODE.to_string(),
            },
        };
        output::output_json(&event);
    }

    // Spawn wormhole sender as background task
    let ticket_str = ticket_str.to_string();
    let relay_url = args.common.wormhole_relay.clone();
    tokio::spawn(async move {
        if let Err(e) = crate::wormhole::send_ticket_via_wormhole(
            &ticket_str,
            relay_url,
            use_json,
        ).await {
            error!("Wormhole sender error: {}", e);
        }
    });

    Ok(())
}

/// Handle direct ticket mode
fn handle_direct_mode(
    args: &HivemindShareArgs,
    ticket_str: &str,
    node_id: &str,
    services: &Services,
    use_json: bool,
) {
    output::display_hub_startup(&args.name, use_json, false, Some(ticket_str));

    if use_json {
        let event = ShareEvent {
            event_type: events::HUB_READY.to_string(),
            timestamp: output::get_current_timestamp(),
            data: ShareEventData {
                hub_name: args.name.clone(),
                ticket: Some(ticket_str.to_string()),
                join_code: None,
                node_id: node_id.to_string(),
                services: services.clone(),
                status: status::DIRECT_MODE.to_string(),
            },
        };
        output::output_json(&event);
    }
}

/// Main hub loop to accept and handle incoming connections
async fn run_hub_loop(endpoint: Endpoint, config: crate::HiveConfig) -> Result<()> {
    loop {
        let incoming = match endpoint.accept().await {
            Some(incoming) => incoming,
            None => {
                warn!("No more incoming connections");
                break;
            }
        };

        let config = config.clone();

        tokio::spawn(async move {
            match incoming.await {
                Ok(connection) => {
                    let remote_id = connection.remote_id();
                    info!("Accepted connection from: {}", remote_id);

                    if let Err(e) = handle_hub_connection(connection, config).await {
                        error!("Error handling connection from {}: {}", remote_id, e);
                    }
                }
                Err(e) => {
                    error!("Failed to accept connection: {}", e);
                }
            }
        });
    }

    Ok(())
}