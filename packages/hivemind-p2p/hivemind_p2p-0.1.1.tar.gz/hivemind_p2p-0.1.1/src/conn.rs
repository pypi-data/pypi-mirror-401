use tokio::net::TcpStream;
use tracing::{debug, warn};

/// Forward data bidirectionally between a TCP stream and a QUIC stream
pub async fn forward_bidi(
    tcp_stream: TcpStream,
    mut quic_send: iroh::endpoint::SendStream,
    mut quic_recv: iroh::endpoint::RecvStream,
) -> anyhow::Result<()> {
    let (mut tcp_read, mut tcp_write) = tcp_stream.into_split();

    // Copy both directions concurrently
    let tcp_to_quic = async {
        match tokio::io::copy(&mut tcp_read, &mut quic_send).await {
            Ok(n) => {
                debug!("TCP->QUIC copied {} bytes", n);
                let _ = quic_send.finish();
                Ok(n)
            }
            Err(e) => {
                warn!("TCP->QUIC error: {}", e);
                Err(e)
            }
        }
    };

    let quic_to_tcp = async {
        match tokio::io::copy(&mut quic_recv, &mut tcp_write).await {
            Ok(n) => {
                debug!("QUIC->TCP copied {} bytes", n);
                let _ = tokio::io::AsyncWriteExt::shutdown(&mut tcp_write).await;
                Ok(n)
            }
            Err(e) => {
                warn!("QUIC->TCP error: {}", e);
                Err(e)
            }
        }
    };

    // Run both directions concurrently
    let (r1, r2) = tokio::join!(tcp_to_quic, quic_to_tcp);

    // Log results but don't fail if one direction had an error
    match r1 {
        Ok(n) => debug!("TCP->QUIC completed: {} bytes", n),
        Err(e) => debug!("TCP->QUIC ended with error: {}", e),
    }
    match r2 {
        Ok(n) => debug!("QUIC->TCP completed: {} bytes", n),
        Err(e) => debug!("QUIC->TCP ended with error: {}", e),
    }

    Ok(())
}
