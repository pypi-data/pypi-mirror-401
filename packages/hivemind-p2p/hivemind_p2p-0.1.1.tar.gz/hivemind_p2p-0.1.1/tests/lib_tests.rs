use hivemind_p2p::*;
use std::net::SocketAddr;

/// Tests for HiveConfig
#[test]
fn test_hive_config_new() {
    let frontend: SocketAddr = "127.0.0.1:3000".parse().unwrap();
    let backend: SocketAddr = "127.0.0.1:8000".parse().unwrap();
    let ws: SocketAddr = "127.0.0.1:4000".parse().unwrap();

    let config = HiveConfig::new(frontend, backend, ws);

    assert_eq!(config.frontend(), frontend);
    assert_eq!(config.backend(), backend);
    assert_eq!(config.websocket(), ws);
}

#[test]
fn test_hive_config_default_localhost() {
    let config = HiveConfig::default_localhost();

    assert_eq!(config.frontend(), "127.0.0.1:3000".parse::<SocketAddr>().unwrap());
    assert_eq!(config.backend(), "127.0.0.1:8000".parse::<SocketAddr>().unwrap());
    assert_eq!(config.websocket(), "127.0.0.1:4000".parse::<SocketAddr>().unwrap());
}

#[test]
fn test_hive_config_get_service_by_port_id() {
    let config = HiveConfig::default_localhost();

    // Valid port IDs
    assert!(config.get_service(PORT_ID_FRONTEND).is_some());
    assert!(config.get_service(PORT_ID_BACKEND).is_some());
    assert!(config.get_service(PORT_ID_WS).is_some());

    // Invalid port IDs
    assert!(config.get_service(0x00).is_none());
    assert!(config.get_service(0x04).is_none());
    assert!(config.get_service(0xFF).is_none());
}

#[test]
fn test_hive_config_port_id_mapping() {
    let frontend: SocketAddr = "10.0.0.1:5000".parse().unwrap();
    let backend: SocketAddr = "10.0.0.2:5001".parse().unwrap();
    let ws: SocketAddr = "10.0.0.3:5002".parse().unwrap();

    let config = HiveConfig::new(frontend, backend, ws);

    // Verify port ID mapping
    assert_eq!(config.get_service(PORT_ID_FRONTEND).unwrap(), frontend);
    assert_eq!(config.get_service(PORT_ID_BACKEND).unwrap(), backend);
    assert_eq!(config.get_service(PORT_ID_WS).unwrap(), ws);
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

/// Tests for protocol constants
#[test]
fn test_port_id_constants() {
    // Ensure port IDs are distinct
    assert_ne!(PORT_ID_FRONTEND, PORT_ID_BACKEND);
    assert_ne!(PORT_ID_FRONTEND, PORT_ID_WS);
    assert_ne!(PORT_ID_BACKEND, PORT_ID_WS);

    // Ensure port IDs are in expected range
    assert!(PORT_ID_FRONTEND > 0);
    assert!(PORT_ID_BACKEND > 0);
    assert!(PORT_ID_WS > 0);

    // Verify specific values (as documented)
    assert_eq!(PORT_ID_FRONTEND, 0x01);
    assert_eq!(PORT_ID_BACKEND, 0x02);
    assert_eq!(PORT_ID_WS, 0x03);
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

#[test]
fn test_default_port_constants() {
    assert_eq!(HIVE_FRONTEND_PORT, 3000);
    assert_eq!(HIVE_BACKEND_PORT, 8000);
    assert_eq!(HIVE_BACKEND_WS_PORT, 4000);
}

#[test]
fn test_default_address_strings() {
    assert_eq!(DEFAULT_FRONTEND_ADDR, "127.0.0.1:3000");
    assert_eq!(DEFAULT_BACKEND_ADDR, "127.0.0.1:8000");
    assert_eq!(DEFAULT_WS_ADDR, "127.0.0.1:4000");
}

#[test]
fn test_default_address_functions() {
    assert_eq!(default_frontend_addr(), "127.0.0.1:3000");
    assert_eq!(default_backend_addr(), "127.0.0.1:8000");
    assert_eq!(default_ws_addr(), "127.0.0.1:4000");
}

#[test]
fn test_default_address_consistency() {
    // Ensure const strings match function outputs
    assert_eq!(DEFAULT_FRONTEND_ADDR, default_frontend_addr());
    assert_eq!(DEFAULT_BACKEND_ADDR, default_backend_addr());
    assert_eq!(DEFAULT_WS_ADDR, default_ws_addr());

    // Ensure addresses are parseable as SocketAddr
    assert!(default_frontend_addr().parse::<SocketAddr>().is_ok());
    assert!(default_backend_addr().parse::<SocketAddr>().is_ok());
    assert!(default_ws_addr().parse::<SocketAddr>().is_ok());
}

/// Tests for ALPN constants
#[test]
fn test_hive_alpn_constant() {
    assert_eq!(HIVE_ALPN, b"HIVEMIND/1.0.0");
    assert_eq!(HIVE_ALPN.len(), 14); // Length check
}

#[test]
fn test_federated_hive_alpn_constant() {
    assert_eq!(FEDERATED_HIVE_ALPN, b"HIVEMIND-FEDERATED/1.0.0");
    assert_eq!(FEDERATED_HIVE_ALPN.len(), 24); // Length check
}

#[test]
fn test_alpn_constants_distinct() {
    assert_ne!(HIVE_ALPN, FEDERATED_HIVE_ALPN);
}

/// Tests for HiveConfig with custom addresses
#[test]
fn test_hive_config_with_different_hosts() {
    let frontend: SocketAddr = "192.168.1.10:3000".parse().unwrap();
    let backend: SocketAddr = "192.168.1.11:8000".parse().unwrap();
    let ws: SocketAddr = "192.168.1.12:4000".parse().unwrap();

    let config = HiveConfig::new(frontend, backend, ws);

    assert_eq!(config.frontend().ip().to_string(), "192.168.1.10");
    assert_eq!(config.backend().ip().to_string(), "192.168.1.11");
    assert_eq!(config.websocket().ip().to_string(), "192.168.1.12");
}

#[test]
fn test_hive_config_with_different_ports() {
    let frontend: SocketAddr = "127.0.0.1:5000".parse().unwrap();
    let backend: SocketAddr = "127.0.0.1:5001".parse().unwrap();
    let ws: SocketAddr = "127.0.0.1:5002".parse().unwrap();

    let config = HiveConfig::new(frontend, backend, ws);

    assert_eq!(config.frontend().port(), 5000);
    assert_eq!(config.backend().port(), 5001);
    assert_eq!(config.websocket().port(), 5002);
}

/// Test that HiveConfig is cloneable
#[test]
fn test_hive_config_clone() {
    let config1 = HiveConfig::default_localhost();
    let config2 = config1.clone();

    assert_eq!(config1.frontend(), config2.frontend());
    assert_eq!(config1.backend(), config2.backend());
    assert_eq!(config1.websocket(), config2.websocket());
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
