use clap::{Parser, Subcommand, ValueEnum};
use std::net::{SocketAddrV4, SocketAddrV6};
use serde::{Deserialize, Serialize};
use crate::{AlpnType, Service};
use anyhow::Result;
use std::net::SocketAddr;

#[derive(Parser, Debug)]
#[clap(name = "hivemind-p2p")]
#[clap(about = "Peer-to-peer port forwarding for Hivemind services")]
pub struct Cli {
    #[clap(subcommand)]
    pub command: Command,
}

#[derive(Subcommand, Debug)]
pub enum Command {
    /// Share local Hivemind services with remote peers (hub mode)
    Share(HivemindShareArgs),
    /// Join a remote Hivemind hub (peer mode)
    Join(HivemindJoinArgs),
}

#[derive(Parser, Debug)]
pub struct CommonArgs {
    /// The ALPN protocol to use
    #[clap(long, value_enum, default_value = "hivemind")]
    pub alpn: AlpnType,

    /// The IPv4 address that the endpoint will listen on.
    ///
    /// If None, defaults to a random free port, but it can be useful to specify a fixed
    /// port, e.g. to configure a firewall rule.
    #[clap(long, default_value = None)]
    pub ipv4_addr: Option<SocketAddrV4>,

    /// The IPv6 address that the endpoint will listen on.
    ///
    /// If None, defaults to a random free port, but it can be useful to specify a fixed
    /// port, e.g. to configure a firewall rule.
    #[clap(long, default_value = None)]
    pub ipv6_addr: Option<SocketAddrV6>,

    /// The verbosity level. Repeat to increase verbosity.
    #[clap(short = 'v', long, action = clap::ArgAction::Count)]
    pub verbose: u8,

    /// Custom Magic Wormhole relay server URL
    #[clap(long)]
    pub wormhole_relay: Option<String>,

    /// Output format for structured data
    #[clap(long, value_enum, default_value = "text")]
    pub output_format: OutputFormat,
}

#[derive(Parser, Debug)]
pub struct HivemindShareArgs {
    /// Name for this hub
    pub name: String,

    /// Address of the frontend service to share
    #[clap(long, default_value = "127.0.0.1:3000")]
    pub frontend_addr: String,

    /// Address of the backend service to share
    #[clap(long, default_value = "127.0.0.1:8000")]
    pub backend_addr: String,

    /// Address of the websocket service to share
    #[clap(long, default_value = "127.0.0.1:4000")]
    pub ws_addr: String,

    /// Use Magic Wormhole for easy join codes
    #[clap(long)]
    pub wormhole: bool,

    #[clap(flatten)]
    pub common: CommonArgs,
}

#[derive(Parser, Debug)]
pub struct HivemindJoinArgs {
    /// Name for this peer
    pub name: String,

    /// The endpoint ticket to connect to (string format)
    #[clap(long, conflicts_with = "join_code")]
    pub ticket: Option<String>,

    /// Magic Wormhole join code (e.g., "5-hamburger-endorse")
    #[clap(long, conflicts_with = "ticket")]
    pub join_code: Option<String>,

    /// Local address to listen on for frontend connections
    #[clap(long, default_value = "127.0.0.1:3000")]
    pub frontend_addr: String,

    /// Local address to listen on for backend connections
    #[clap(long, default_value = "127.0.0.1:8000")]
    pub backend_addr: String,

    /// Local address to listen on for websocket connections
    #[clap(long, default_value = "127.0.0.1:4000")]
    pub ws_addr: String,

    #[clap(flatten)]
    pub common: CommonArgs,
}

/// Create configuration from command line arguments
pub fn create_hive_config(args: &HivemindShareArgs) -> Result<crate::HiveConfig> {
    let frontend_addr: SocketAddr = args.frontend_addr.parse()?;
    let backend_addr: SocketAddr = args.backend_addr.parse()?;
    let ws_addr: SocketAddr = args.ws_addr.parse()?;

    // create vec of services
    let services = vec![
        Service {
            label: "frontend".to_string(),
            addr: frontend_addr,
        },
        Service {
            label: "backend".to_string(),
            addr: backend_addr,
        },
        Service {
            label: "websocket".to_string(),
            addr: ws_addr,
        },
    ];
    
    Ok(crate::HiveConfig::new(services))
}

#[derive(ValueEnum, Clone, Debug, PartialEq)]
pub enum OutputFormat {
    /// Human-readable text output
    Text,
    /// Structured JSON output
    Json,
}

#[derive(Clone, Serialize, Deserialize, Debug)]
pub struct Services {
    // list of service labels and their addresses
    pub services: Vec<Service>,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ShareEvent {
    pub event_type: String,
    pub timestamp: String,
    pub data: ShareEventData,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ShareEventData {
    pub hub_name: String,
    pub ticket: Option<String>,
    pub join_code: Option<String>,
    pub node_id: String,
    pub services: Services,
    pub status: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct JoinEvent {
    pub event_type: String,
    pub timestamp: String,
    pub data: JoinEventData,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct JoinEventData {
    pub peer_name: String,
    pub hub_id: Option<String>,
    pub local_services: Services,
    pub status: String,
}