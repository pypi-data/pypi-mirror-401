use serde::{Deserialize, Serialize};

// Hub and peer alpn, peers connect to hubs using this alpn.
pub const HIVE_ALPN: &[u8] = b"HIVEMIND/1.0.0";

// Multi-hub alpn, hubs connect to each other using this alpn.
pub const FEDERATED_HIVE_ALPN: &[u8] = b"HIVEMIND-FEDERATED/1.0.0";

/// Service configuration for hivemind p2p
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Service {
    pub label: String,
    pub addr: std::net::SocketAddr,
}

/// Configuration for hivemind p2p service ports
#[derive(Debug, Clone)]
pub struct HiveConfig {
    /// Array of service objects
    pub services: Vec<Service>,
}

impl HiveConfig {
    /// Create a new HiveConfig with the given service addresses
    pub fn new(
        // map of service to label
        services: Vec<Service>,
    ) -> Self {
        Self { services  }
    }

    pub fn get_services(&self) -> &[Service] {
        &self.services
    }

    pub fn get_service_by_label(&self, label: &str) -> Option<&Service> {
        self.services.iter().find(|s| s.label == label)
    }

    pub fn get_service(&self, port_id: u8) -> Option<std::net::SocketAddr> {
        self.services.get(port_id as usize).map(|s| s.addr)
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