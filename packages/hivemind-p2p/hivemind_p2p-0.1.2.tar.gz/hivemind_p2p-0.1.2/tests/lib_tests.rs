use hivemind_p2p::*;
use std::net::SocketAddr;

/// Tests for HiveConfig
#[test]
fn test_hive_config_new() {
    let frontend: SocketAddr = "127.0.0.1:3000".parse().unwrap();
    let backend: SocketAddr = "127.0.0.1:8000".parse().unwrap();
    let ws: SocketAddr = "127.0.0.1:4000".parse().unwrap();

    let services = vec![
        Service { label: "frontend".to_string(), addr: frontend },
        Service { label: "backend".to_string(), addr: backend },
        Service { label: "websocket".to_string(), addr: ws },
    ];
    let config = HiveConfig::new(services);

    assert_eq!(config.get_service(0).unwrap(), frontend);
    assert_eq!(config.get_service(1).unwrap(), backend);
    assert_eq!(config.get_service(2).unwrap(), ws);
}

#[test]
fn test_hive_config_default_services() {
    let services = vec![
        Service { label: "frontend".to_string(), addr: "127.0.0.1:3000".parse().unwrap() },
        Service { label: "backend".to_string(), addr: "127.0.0.1:8000".parse().unwrap() },
        Service { label: "websocket".to_string(), addr: "127.0.0.1:4000".parse().unwrap() },
    ];
    let config = HiveConfig::new(services);

    assert_eq!(config.get_service(0).unwrap(), "127.0.0.1:3000".parse::<SocketAddr>().unwrap());
    assert_eq!(config.get_service(1).unwrap(), "127.0.0.1:8000".parse::<SocketAddr>().unwrap());
    assert_eq!(config.get_service(2).unwrap(), "127.0.0.1:4000".parse::<SocketAddr>().unwrap());
}

#[test]
fn test_hive_config_get_service_by_port_id() {
    let services = vec![
        Service { label: "frontend".to_string(), addr: "127.0.0.1:3000".parse().unwrap() },
        Service { label: "backend".to_string(), addr: "127.0.0.1:8000".parse().unwrap() },
        Service { label: "websocket".to_string(), addr: "127.0.0.1:4000".parse().unwrap() },
    ];
    let config = HiveConfig::new(services);

    // Valid port IDs (indices 0, 1, 2)
    assert!(config.get_service(0).is_some()); // frontend
    assert!(config.get_service(1).is_some()); // backend
    assert!(config.get_service(2).is_some()); // websocket

    // Invalid port IDs
    assert!(config.get_service(3).is_none());
    assert!(config.get_service(255).is_none());
}

#[test]
fn test_hive_config_port_id_mapping() {
    let frontend: SocketAddr = "10.0.0.1:5000".parse().unwrap();
    let backend: SocketAddr = "10.0.0.2:5001".parse().unwrap();
    let ws: SocketAddr = "10.0.0.3:5002".parse().unwrap();

    let services = vec![
        Service { label: "frontend".to_string(), addr: frontend },
        Service { label: "backend".to_string(), addr: backend },
        Service { label: "websocket".to_string(), addr: ws },
    ];
    let config = HiveConfig::new(services);

    // Verify port ID mapping (index-based)
    assert_eq!(config.get_service(0).unwrap(), frontend); // frontend = index 0
    assert_eq!(config.get_service(1).unwrap(), backend);  // backend = index 1
    assert_eq!(config.get_service(2).unwrap(), ws);       // websocket = index 2
}

/// Tests for AlpnType
#[test]
fn test_alpn_type_hivemind_bytes() {
    let alpn = AlpnType::Hivemind;
    assert_eq!(alpn.as_bytes(), HIVE_ALPN);
    assert_eq!(alpn.as_bytes(), b"HIVEMIND/1.0.0");
}

#[test]
fn test_alpn_type_federated_hivemind_bytes() {
    let alpn = AlpnType::FederatedHivemind;
    assert_eq!(alpn.as_bytes(), FEDERATED_HIVE_ALPN);
    assert_eq!(alpn.as_bytes(), b"HIVEMIND-FEDERATED/1.0.0");
}

#[test]
fn test_alpn_type_equality() {
    assert_eq!(AlpnType::Hivemind, AlpnType::Hivemind);
    assert_eq!(AlpnType::FederatedHivemind, AlpnType::FederatedHivemind);
    assert_ne!(AlpnType::Hivemind, AlpnType::FederatedHivemind);
}

/// Tests for service configuration
#[test]
fn test_hive_config_get_service_by_label() {
    let services = vec![
        Service { label: "frontend".to_string(), addr: "127.0.0.1:3000".parse().unwrap() },
        Service { label: "backend".to_string(), addr: "127.0.0.1:8000".parse().unwrap() },
        Service { label: "websocket".to_string(), addr: "127.0.0.1:4000".parse().unwrap() },
    ];
    let config = HiveConfig::new(services);

    // Test get_service_by_label function
    assert!(config.get_service_by_label("frontend").is_some());
    assert!(config.get_service_by_label("backend").is_some());
    assert!(config.get_service_by_label("websocket").is_some());
    assert!(config.get_service_by_label("unknown").is_none());

    // Verify correct addresses
    assert_eq!(config.get_service_by_label("frontend").unwrap().addr, "127.0.0.1:3000".parse().unwrap());
    assert_eq!(config.get_service_by_label("backend").unwrap().addr, "127.0.0.1:8000".parse().unwrap());
    assert_eq!(config.get_service_by_label("websocket").unwrap().addr, "127.0.0.1:4000".parse().unwrap());
}

#[test]
fn test_ack_constants() {
    // ACK constants should be distinct
    assert_ne!(ACK_SUCCESS, ACK_ERROR);

    // Verify specific values (as documented)
    assert_eq!(ACK_SUCCESS, 0xFF);
    assert_eq!(ACK_ERROR, 0x00);
}

#[test]
fn test_handshake_constant() {
    // Verify handshake is 11 bytes
    assert_eq!(HANDSHAKE.len(), 11);

    // Verify handshake content
    assert_eq!(HANDSHAKE, *b"hivemindp2p");
    assert_eq!(&HANDSHAKE, b"hivemindp2p");
}

/// Tests for HiveConfig with custom addresses
#[test]
fn test_hive_config_with_different_hosts() {
    let frontend: SocketAddr = "192.168.1.10:3000".parse().unwrap();
    let backend: SocketAddr = "192.168.1.11:8000".parse().unwrap();
    let ws: SocketAddr = "192.168.1.12:4000".parse().unwrap();

    let services = vec![
        Service { label: "frontend".to_string(), addr: frontend },
        Service { label: "backend".to_string(), addr: backend },
        Service { label: "websocket".to_string(), addr: ws },
    ];
    let config = HiveConfig::new(services);

    assert_eq!(config.get_service(0).unwrap().ip().to_string(), "192.168.1.10");
    assert_eq!(config.get_service(1).unwrap().ip().to_string(), "192.168.1.11");
    assert_eq!(config.get_service(2).unwrap().ip().to_string(), "192.168.1.12");
}

#[test]
fn test_hive_config_with_different_ports() {
    let frontend: SocketAddr = "127.0.0.1:5000".parse().unwrap();
    let backend: SocketAddr = "127.0.0.1:5001".parse().unwrap();
    let ws: SocketAddr = "127.0.0.1:5002".parse().unwrap();

    let services = vec![
        Service { label: "frontend".to_string(), addr: frontend },
        Service { label: "backend".to_string(), addr: backend },
        Service { label: "websocket".to_string(), addr: ws },
    ];
    let config = HiveConfig::new(services);

    assert_eq!(config.get_service(0).unwrap().port(), 5000);
    assert_eq!(config.get_service(1).unwrap().port(), 5001);
    assert_eq!(config.get_service(2).unwrap().port(), 5002);
}

/// Test that HiveConfig is cloneable
#[test]
fn test_hive_config_clone() {
    let services = vec![
        Service { label: "frontend".to_string(), addr: "127.0.0.1:3000".parse().unwrap() },
        Service { label: "backend".to_string(), addr: "127.0.0.1:8000".parse().unwrap() },
        Service { label: "websocket".to_string(), addr: "127.0.0.1:4000".parse().unwrap() },
    ];
    let config1 = HiveConfig::new(services);
    let config2 = config1.clone();

    assert_eq!(config1.get_service(0).unwrap(), config2.get_service(0).unwrap());
    assert_eq!(config1.get_service(1).unwrap(), config2.get_service(1).unwrap());
    assert_eq!(config1.get_service(2).unwrap(), config2.get_service(2).unwrap());
}

/// Test that AlpnType is Copy
#[test]
fn test_alpn_type_copy() {
    let alpn1 = AlpnType::Hivemind;
    let alpn2 = alpn1; // Copy
    assert_eq!(alpn1, alpn2);
    // alpn1 is still usable after copy
    assert_eq!(alpn1.as_bytes(), HIVE_ALPN);
}
