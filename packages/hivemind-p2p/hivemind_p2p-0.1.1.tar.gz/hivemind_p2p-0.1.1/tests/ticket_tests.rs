use hivemind_p2p::EndpointTicket;
use iroh::{Endpoint, SecretKey};

#[tokio::test]
async fn test_ticket_create_and_parse() -> anyhow::Result<()> {
    // Create endpoint
    let secret_key = SecretKey::generate(&mut rand::rng());
    let endpoint = Endpoint::builder()
        .secret_key(secret_key)
        .bind()
        .await?;

    let endpoint_addr = endpoint.addr();

    // Create ticket
    let ticket = EndpointTicket::new(endpoint_addr.clone());
    let ticket_str = ticket.to_string();

    // Parse ticket back
    let parsed_ticket: EndpointTicket = ticket_str.parse()?;
    let parsed_addr = parsed_ticket.endpoint_addr();

    // Verify node ID matches
    assert_eq!(endpoint_addr.id, parsed_addr.id);

    Ok(())
}

#[tokio::test]
async fn test_ticket_invalid_format() {
    let result: Result<EndpointTicket, _> = "invalid-ticket-string".parse();
    assert!(result.is_err());
}
