use anyhow::{Context, Result};
use magic_wormhole::{transfer, AppConfig, Code, MailboxConnection, Wormhole};
use serde_json;
use std::str::FromStr;
use tokio::time::{sleep, Duration};
use tracing::{error, info};

/// Send a ticket string via Magic Wormhole, generating rotating join codes.
///
/// This function loops indefinitely, generating a new join code every 500ms.
/// Each code allows one peer to connect and receive the ticket.
///
/// # Arguments
/// * `ticket` - The EndpointTicket string to send
/// * `relay_url` - Optional custom Magic Wormhole relay server URL
/// * `use_json` - Whether to output structured JSON events
pub async fn send_ticket_via_wormhole(ticket: &str, relay_url: Option<String>, use_json: bool) -> Result<()> {
    let config = build_wormhole_config(relay_url)?;
    let payload = ticket.as_bytes().to_vec();

    info!("Starting Magic Wormhole sender loop");

    loop {
        // Create a new mailbox connection (generates a fresh join code)
        let mailbox_connection = match MailboxConnection::create(config.clone(), 2).await {
            Ok(mc) => mc,
            Err(e) => {
                error!("Failed to create mailbox connection: {}", e);
                sleep(Duration::from_millis(500)).await;
                continue;
            }
        };

        let code = mailbox_connection.code().clone();

        // Output join code based on format preference
        if use_json {
            let join_code_event = serde_json::json!({
                "event_type": "join_code",
                "timestamp": std::time::SystemTime::now()
                    .duration_since(std::time::UNIX_EPOCH)
                    .unwrap()
                    .as_secs(),
                "data": {
                    "join_code": code.to_string(),
                    "status": "waiting_for_connection"
                }
            });
            println!("{}", join_code_event);
        } else {
            // Print the join code in a prominent box
            println!("\n┌────────────────────────────────────────┐");
            println!("│  Join code: {}  │", code);
            println!("└────────────────────────────────────────┘");
            println!("Waiting for peer to connect...");
        }

        // Establish wormhole connection
        let mut wormhole = match Wormhole::connect(mailbox_connection).await {
            Ok(w) => w,
            Err(e) => {
                error!("Failed to establish wormhole connection: {}", e);
                sleep(Duration::from_millis(500)).await;
                continue;
            }
        };

        info!("Wormhole connected, sending ticket");

        // Send the ticket payload
        match wormhole.send(payload.clone()).await {
            Ok(_) => {
                info!("Ticket sent successfully via wormhole");
                if use_json {
                    let success_event = serde_json::json!({
                        "event_type": "peer_connected",
                        "timestamp": std::time::SystemTime::now()
                            .duration_since(std::time::UNIX_EPOCH)
                            .unwrap()
                            .as_secs(),
                        "data": {
                            "join_code": code.to_string(),
                            "status": "connected"
                        }
                    });
                    println!("{}", success_event);
                } else {
                    println!("✓ Peer connected and received ticket\n");
                }
            }
            Err(e) => {
                error!("Failed to send ticket: {}", e);
            }
        }

        // Sleep before generating next code
        sleep(Duration::from_millis(500)).await;
    }
}

/// Receive a ticket string via Magic Wormhole using a join code.
///
/// # Arguments
/// * `join_code` - The join code to connect with (e.g., "5-hamburger-endorse")
/// * `relay_url` - Optional custom Magic Wormhole relay server URL
///
/// # Returns
/// The EndpointTicket string received from the hub
pub async fn receive_ticket_via_wormhole(
    join_code: &str,
    relay_url: Option<String>,
) -> Result<String> {
    let config = build_wormhole_config(relay_url)?;

    // Parse the join code
    let code = Code::from_str(join_code).context("Invalid join code format. Expected format like '5-hamburger-endorse'")?;

    info!("Connecting to wormhole with code: {}", join_code);
    println!("Connecting to Magic Wormhole...");

    // Connect to mailbox with the code
    let mailbox_connection = MailboxConnection::connect(config, code, false)
        .await
        .context("Failed to connect to wormhole server. Check your internet connection and try again.")?;

    // Establish wormhole connection
    let mut wormhole = Wormhole::connect(mailbox_connection)
        .await
        .context("Failed to establish wormhole connection. Did the hub stop running?")?;

    info!("Wormhole connected, receiving ticket");
    println!("Connected! Receiving ticket...");

    // Receive the ticket bytes
    let ticket_bytes = wormhole
        .receive()
        .await
        .context("Failed to receive ticket data. Connection may have been interrupted.")?;

    // Convert to UTF-8 string
    let ticket_str = String::from_utf8(ticket_bytes)
        .context("Received invalid ticket data (not valid UTF-8)")?;

    info!("Ticket received successfully");
    println!("✓ Ticket received!\n");

    Ok(ticket_str)
}

/// Build a Magic Wormhole configuration.
///
/// # Arguments
/// * `relay_url` - Optional custom relay server URL. If None, uses default public servers.
///
/// # Returns
/// An AppConfig configured for hivemind-p2p
fn build_wormhole_config(_relay_url: Option<String>) -> Result<AppConfig<transfer::AppVersion>> {
    // Use default transfer config
    // Note: Custom relay URL support may require magic-wormhole 0.8+
    // For now, we use the default public servers
    let config = transfer::APP_CONFIG;

    Ok(config)
}
