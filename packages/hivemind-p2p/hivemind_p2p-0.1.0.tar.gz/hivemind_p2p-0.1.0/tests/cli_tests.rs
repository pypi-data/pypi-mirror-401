use clap::Parser;
use hivemind_p2p::cli::{Cli, Command};

#[test]
fn test_share_command_parsing() {
    let args = vec![
        "hivemind-p2p",
        "share",
        "test-hub",
        "--frontend-addr",
        "127.0.0.1:3000",
        "--backend-addr",
        "127.0.0.1:8000",
        "--ws-addr",
        "127.0.0.1:4000",
        "--wormhole",
    ];

    let cli = Cli::parse_from(args);

    match cli.command {
        Command::Share(share_args) => {
            assert_eq!(share_args.name, "test-hub");
            assert_eq!(share_args.frontend_addr, "127.0.0.1:3000");
            assert_eq!(share_args.backend_addr, "127.0.0.1:8000");
            assert_eq!(share_args.ws_addr, "127.0.0.1:4000");
            assert!(share_args.wormhole);
        }
        _ => panic!("Expected Share command"),
    }
}

#[test]
fn test_share_command_with_defaults() {
    let args = vec![
        "hivemind-p2p",
        "share",
        "test-hub",
    ];

    let cli = Cli::parse_from(args);

    match cli.command {
        Command::Share(share_args) => {
            assert_eq!(share_args.name, "test-hub");
            assert_eq!(share_args.frontend_addr, "127.0.0.1:3000");
            assert_eq!(share_args.backend_addr, "127.0.0.1:8000");
            assert_eq!(share_args.ws_addr, "127.0.0.1:4000");
            assert!(!share_args.wormhole);
        }
        _ => panic!("Expected Share command"),
    }
}

#[test]
fn test_join_command_with_ticket() {
    let args = vec![
        "hivemind-p2p",
        "join",
        "test-peer",
        "--ticket",
        "fake-ticket-string",
    ];

    let cli = Cli::parse_from(args);

    match cli.command {
        Command::Join(join_args) => {
            assert_eq!(join_args.name, "test-peer");
            assert_eq!(join_args.ticket, Some("fake-ticket-string".to_string()));
            assert_eq!(join_args.join_code, None);
        }
        _ => panic!("Expected Join command"),
    }
}

#[test]
fn test_join_command_with_join_code() {
    let args = vec![
        "hivemind-p2p",
        "join",
        "test-peer",
        "--join-code",
        "5-hamburger-endorse",
    ];

    let cli = Cli::parse_from(args);

    match cli.command {
        Command::Join(join_args) => {
            assert_eq!(join_args.name, "test-peer");
            assert_eq!(join_args.join_code, Some("5-hamburger-endorse".to_string()));
            assert_eq!(join_args.ticket, None);
        }
        _ => panic!("Expected Join command"),
    }
}

#[test]
fn test_ticket_and_join_code_conflict() {
    // This should fail parsing due to conflicts_with constraint
    let args = vec![
        "hivemind-p2p",
        "join",
        "test-peer",
        "--ticket",
        "ticket",
        "--join-code",
        "5-code-word",
    ];

    let result = Cli::try_parse_from(args);
    assert!(result.is_err(), "Expected parsing to fail due to conflicts_with constraint");
}
