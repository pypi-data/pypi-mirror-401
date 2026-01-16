// Hub and peer alpn, peers connect to hubs using this alpn.
pub const HIVE_ALPN: &[u8] = b"HIVEMIND/1.0.0";

// Multi-hub alpn, hubs connect to each other using this alpn.
pub const FEDERATED_HIVE_ALPN: &[u8] = b"HIVEMIND-FEDERATED/1.0.0";

// Default ports - single source of truth
pub const HIVE_FRONTEND_PORT: u16 = 3000;
pub const HIVE_BACKEND_PORT: u16 = 8000;
pub const HIVE_BACKEND_WS_PORT: u16 = 4000;

// Default address strings for clap (const strings required for default_value)
pub const DEFAULT_FRONTEND_ADDR: &str = "127.0.0.1:3000";
pub const DEFAULT_BACKEND_ADDR: &str = "127.0.0.1:8000";
pub const DEFAULT_WS_ADDR: &str = "127.0.0.1:4000";

// Helper functions to construct default addresses from port constants
pub fn default_frontend_addr() -> String {
    format!("127.0.0.1:{}", HIVE_FRONTEND_PORT)
}

pub fn default_backend_addr() -> String {
    format!("127.0.0.1:{}", HIVE_BACKEND_PORT)
}

pub fn default_ws_addr() -> String {
    format!("127.0.0.1:{}", HIVE_BACKEND_WS_PORT)
}

/// Configuration for hivemind p2p service ports
#[derive(Debug, Clone)]
pub struct HiveConfig {
    /// Array of service addresses indexed by port ID
    /// Index 0 is unused, indices 1-3 correspond to PORT_ID_FRONTEND, PORT_ID_BACKEND, PORT_ID_WS
    services: [std::net::SocketAddr; 4],
}

impl HiveConfig {
    /// Create a new HiveConfig with the given service addresses
    pub fn new(
        frontend_addr: std::net::SocketAddr,
        backend_addr: std::net::SocketAddr,
        ws_addr: std::net::SocketAddr,
    ) -> Self {
        let services = [
            "0.0.0.0:0".parse().unwrap(),  // Index 0 unused
            frontend_addr,                 // Index 1 (PORT_ID_FRONTEND)
            backend_addr,                  // Index 2 (PORT_ID_BACKEND)
            ws_addr,                       // Index 3 (PORT_ID_WS)
        ];
        Self { services }
    }

    /// Create a HiveConfig with default localhost addresses
    pub fn default_localhost() -> Self {
        Self::new(
            default_frontend_addr().parse().unwrap(),
            default_backend_addr().parse().unwrap(),
            default_ws_addr().parse().unwrap(),
        )
    }

    /// Get the service address for a given port ID
    pub fn get_service(&self, port_id: u8) -> Option<std::net::SocketAddr> {
        match port_id {
            PORT_ID_FRONTEND | PORT_ID_BACKEND | PORT_ID_WS => {
                Some(self.services[port_id as usize])
            }
            _ => None,
        }
    }

    /// Get the frontend service address
    pub fn frontend(&self) -> std::net::SocketAddr {
        self.services[PORT_ID_FRONTEND as usize]
    }

    /// Get the backend service address
    pub fn backend(&self) -> std::net::SocketAddr {
        self.services[PORT_ID_BACKEND as usize]
    }

    /// Get the websocket service address
    pub fn websocket(&self) -> std::net::SocketAddr {
        self.services[PORT_ID_WS as usize]
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, clap::ValueEnum)]
pub enum AlpnType {
    Hivemind,
    FederatedHivemind,
}

impl AlpnType {
    pub fn as_bytes(&self) -> &'static [u8] {
        match self {
            AlpnType::Hivemind => HIVE_ALPN,
            AlpnType::FederatedHivemind => FEDERATED_HIVE_ALPN,
        }
    }
}

/// The handshake to send when connecting.
///
/// The side that calls open_bi() first must send this handshake, the side that
/// calls accept_bi() must consume it.
pub const HANDSHAKE: [u8; 11] = *b"hivemindp2p";

/// Port identifier for frontend service (default port 3000)
pub const PORT_ID_FRONTEND: u8 = 0x01;

/// Port identifier for backend service (default port 8000)
pub const PORT_ID_BACKEND: u8 = 0x02;

/// Port identifier for websocket service (default port 4000)
pub const PORT_ID_WS: u8 = 0x03;

/// ACK byte sent by hub to indicate successful stream setup
pub const ACK_SUCCESS: u8 = 0xFF;

/// ACK byte sent by hub to indicate error in stream setup
pub const ACK_ERROR: u8 = 0x00;

// Re-export ticket type for convenience
pub use iroh_tickets::endpoint::EndpointTicket;

pub mod cli;
pub mod conn;
pub mod wormhole;
pub mod output;
pub mod handlers;
pub mod hub;
pub mod peer;