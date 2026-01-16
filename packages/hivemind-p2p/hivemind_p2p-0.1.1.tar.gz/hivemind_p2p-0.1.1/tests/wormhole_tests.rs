use tokio::time::Duration;

#[tokio::test]
#[ignore] // Requires network access to Magic Wormhole servers
async fn test_wormhole_roundtrip() -> anyhow::Result<()> {
    let test_ticket = "test-endpoint-ticket-abc123";

    // Spawn sender task
    let ticket_clone = test_ticket.to_string();
    let sender_handle = tokio::spawn(async move {
        // Send will loop, but we only care about first code generation
        if let Err(e) = hivemind_p2p::wormhole::send_ticket_via_wormhole(&ticket_clone, None, false).await {
            eprintln!("Sender error: {}", e);
        }
    });

    // Give sender time to generate join code
    tokio::time::sleep(Duration::from_millis(100)).await;

    // In real test, we'd need to capture the printed join code
    // For now, this tests compilation and basic flow
    // TODO: Refactor wormhole.rs to return join code instead of printing

    // Cleanup
    sender_handle.abort();

    Ok(())
}
