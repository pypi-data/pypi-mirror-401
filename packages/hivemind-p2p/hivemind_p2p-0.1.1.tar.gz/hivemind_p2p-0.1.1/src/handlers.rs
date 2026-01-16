use anyhow::Result;
use iroh::endpoint::Connection;
use tokio::net::TcpStream;
use tracing::{info, warn, error, debug};

use crate::{HiveConfig, PORT_ID_FRONTEND, PORT_ID_BACKEND, PORT_ID_WS, HANDSHAKE, ACK_SUCCESS, ACK_ERROR};

/// Get service name from port ID for logging
pub fn get_service_name(port_id: u8) -> &'static str {
    match port_id {
        PORT_ID_FRONTEND => "frontend",
        PORT_ID_BACKEND => "backend", 
        PORT_ID_WS => "websocket",
        _ => "unknown",
    }
}

/// Handle a single hub connection from a peer
pub async fn handle_hub_connection(
    connection: Connection,
    config: HiveConfig,
) -> Result<()> {
    let remote_id = connection.remote_id();

    // Accept and handle multiple streams from this peer
    loop {
        let (mut send, mut recv) = match connection.accept_bi().await {
            Ok(streams) => streams,
            Err(e) => {
                debug!("Connection closed or no more streams from {}: {}", remote_id, e);
                break;
            }
        };

        // Read port ID byte
        let mut port_id_buf = [0u8; 1];
        if recv.read_exact(&mut port_id_buf).await.is_err() {
            warn!("Failed to read port ID from {}", remote_id);
            let _ = send.write_all(&[ACK_ERROR]).await;
            continue;
        }
        let port_id = port_id_buf[0];

        // Read handshake
        let mut handshake_buf = [0u8; 11];
        if recv.read_exact(&mut handshake_buf).await.is_err() || handshake_buf != HANDSHAKE {
            warn!("Invalid handshake from {}", remote_id);
            let _ = send.write_all(&[ACK_ERROR]).await;
            continue;
        }

        // Handle the validated request
        let service_name = get_service_name(port_id);
        let target_addr = match config.get_service(port_id) {
            Some(addr) => {
                info!("Peer {} requesting {} stream", remote_id, service_name);
                addr
            }
            None => {
                warn!("Unknown port ID {} from {}", port_id, remote_id);
                let _ = send.write_all(&[ACK_ERROR]).await;
                continue;
            }
        };

        // Send ACK
        if send.write_all(&[ACK_SUCCESS]).await.is_err() {
            warn!("Failed to send ACK to {}", remote_id);
            continue;
        }

        // Connect to local service
        let tcp_stream = match TcpStream::connect(target_addr).await {
            Ok(s) => s,
            Err(e) => {
                error!("Failed to connect to {}: {}", target_addr, e);
                continue;
            }
        };

        info!("Connected to {} for peer {}", target_addr, remote_id);

        // Spawn bidirectional forwarding
        tokio::spawn(async move {
            if let Err(e) = crate::conn::forward_bidi(tcp_stream, send, recv).await {
                debug!("Stream forwarding ended: {}", e);
            }
        });
    }

    info!("Connection from {} closed", remote_id);
    Ok(())
}

/// Handle a single peer listener (frontend, backend, or websocket)
pub async fn handle_peer_listener(
    connection: Connection,
    listener: tokio::net::TcpListener,
    port_id: u8,
) -> Result<()> {
    let port_name = get_service_name(port_id);

    loop {
        let (tcp_stream, tcp_addr) = listener.accept().await?;
        info!("Accepted local {} connection from {}", port_name, tcp_addr);

        if let Err(e) = establish_hub_stream(
            &connection,
            tcp_stream,
            port_id,
            port_name
        ).await {
            warn!("Failed to establish {} stream: {}", port_name, e);
        }
    }
}

/// Establish a new stream to the hub for a local connection
async fn establish_hub_stream(
    connection: &Connection,
    tcp_stream: TcpStream,
    port_id: u8,
    port_name: &str,
) -> Result<()> {
    // Open bidirectional stream to hub
    let (mut send, mut recv) = connection.open_bi().await?;

    // Send port ID and handshake
    send.write_all(&[port_id]).await?;
    send.write_all(&HANDSHAKE).await?;

    // Wait for ACK
    let mut ack_buf = [0u8; 1];
    recv.read_exact(&mut ack_buf).await?;

    if ack_buf[0] != ACK_SUCCESS {
        anyhow::bail!("Hub rejected {} stream", port_name);
    }

    debug!("Hub accepted {} stream", port_name);

    // Spawn bidirectional forwarding
    tokio::spawn(async move {
        if let Err(e) = crate::conn::forward_bidi(tcp_stream, send, recv).await {
            debug!("Stream forwarding ended: {}", e);
        }
    });

    Ok(())
}