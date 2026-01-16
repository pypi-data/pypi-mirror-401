use axum::{routing::get, Router};
use hivemind_p2p::{HANDSHAKE, PORT_ID_FRONTEND, ACK_SUCCESS};
use iroh::{Endpoint, SecretKey};
use std::net::SocketAddr;
use tokio::time::Duration;

// These trait imports are required for read_exact() and write_all()
#[allow(unused_imports)]
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[tokio::test]
async fn test_http_through_tunnel_handshake() -> anyhow::Result<()> {
    // 1. Start a simple HTTP server (simulates the hub's frontend service)
    let app = Router::new().route("/", get(|| async { "Hello from hub!" }));
    let server_addr: SocketAddr = "127.0.0.1:0".parse()?; // Random port
    let listener = tokio::net::TcpListener::bind(server_addr).await?;
    let actual_server_addr = listener.local_addr()?;

    tokio::spawn(async move {
        axum::serve(listener, app).await.unwrap();
    });

    // Give server time to start
    tokio::time::sleep(Duration::from_millis(50)).await;

    // 2. Create hub endpoint
    let hub_secret = SecretKey::generate(&mut rand::rng());
    let hub_endpoint = Endpoint::builder()
        .secret_key(hub_secret)
        .alpns(vec![b"HIVEMIND/1.0.0".to_vec()])
        .bind()
        .await?;

    let hub_addr = hub_endpoint.addr();

    // 3. Spawn simplified hub connection handler
    let server_addr_clone = actual_server_addr;
    let hub_conn_handler = tokio::spawn(async move {
        if let Some(incoming) = hub_endpoint.accept().await {
            if let Ok(connection) = incoming.await {
                // Accept one stream
                if let Ok((mut send, mut recv)) = connection.accept_bi().await {
                    // Read port ID
                    let mut port_id = [0u8; 1];
                    recv.read_exact(&mut port_id).await.unwrap();

                    // Read handshake
                    let mut handshake_buf = [0u8; 11];
                    recv.read_exact(&mut handshake_buf).await.unwrap();

                    if handshake_buf == HANDSHAKE && port_id[0] == PORT_ID_FRONTEND {
                        // Send ACK
                        send.write_all(&[ACK_SUCCESS]).await.unwrap();

                        // Connect to HTTP server and forward (simplified)
                        let tcp_stream = tokio::net::TcpStream::connect(server_addr_clone).await.unwrap();
                        tokio::spawn(hivemind_p2p::conn::forward_bidi(tcp_stream, send, recv));
                    }
                }
            }
        }
    });

    // 4. Create peer endpoint and connect
    let peer_secret = SecretKey::generate(&mut rand::rng());
    let peer_endpoint = Endpoint::builder()
        .secret_key(peer_secret)
        .alpns(vec![b"HIVEMIND/1.0.0".to_vec()])
        .bind()
        .await?;

    let connection = peer_endpoint
        .connect(hub_addr, b"HIVEMIND/1.0.0")
        .await?;

    // 5. Open stream to hub
    let (mut send, mut recv) = connection.open_bi().await?;

    // Send handshake
    send.write_all(&[PORT_ID_FRONTEND]).await?;
    send.write_all(&HANDSHAKE).await?;

    // Wait for ACK
    let mut ack = [0u8; 1];
    recv.read_exact(&mut ack).await?;
    assert_eq!(ack[0], ACK_SUCCESS);

    // Test passes if we successfully got ACK
    hub_conn_handler.abort();

    Ok(())
}
