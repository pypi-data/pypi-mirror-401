use std::time::{SystemTime, UNIX_EPOCH};
use tracing::info;

/// Event types for JSON output
pub mod events {
    pub const HUB_READY: &str = "hub_ready";
    pub const PEER_CONNECTED: &str = "peer_connected";
}

/// Status values for JSON output
pub mod status {
    pub const WORMHOLE_MODE: &str = "wormhole_mode";
    pub const DIRECT_MODE: &str = "direct_mode";
    pub const CONNECTED: &str = "connected";
}

/// Initialize logging based on verbosity level
pub fn init_logging(verbose: u8) {
    let log_level = match verbose {
        0 => "error",
        1 => "warn", 
        2 => "info",
        3 => "debug",
        _ => "trace",
    };
    
    tracing_subscriber::fmt()
        .with_env_filter(log_level)
        .with_writer(std::io::stderr)
        .init();
}

/// Get current timestamp as string
pub fn get_current_timestamp() -> String {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs()
        .to_string()
}

/// Output JSON events to stdout
pub fn output_json<T: serde::Serialize>(event: &T) {
    if let Ok(json) = serde_json::to_string(event) {
        println!("{}", json);
    }
}

/// Display a formatted box with title
pub fn display_box(title: &str) {
    println!("\n╔══════════════════════════════════════════════════════════════════════════════╗");
    println!("║ {:<76} ║", title);
    println!("╚══════════════════════════════════════════════════════════════════════════════╝");
}

/// Log message based on output format (JSON mode uses eprintln!, normal mode uses tracing)
pub fn log_info(message: &str, use_json: bool) {
    if use_json {
        eprintln!("{}", message);
    } else {
        info!("{}", message);
    }
}

/// Display hub startup information
pub fn display_hub_startup(name: &str, use_json: bool, wormhole_mode: bool, ticket: Option<&str>) {
    if use_json {
        let mode = if wormhole_mode { "Magic Wormhole" } else { "direct ticket" };
        log_info(&format!("Hub '{}' starting with {}", name, mode), true);
        if wormhole_mode {
            log_info(&format!("Generating join codes for peers to connect..."), true);
        }
    } else {
        if wormhole_mode {
            display_box(&format!("Hub '{}' starting with Magic Wormhole", name));
            println!("\nGenerating join codes for peers to connect...");
        } else {
            display_box(&format!("Hub '{}' is running", name));
            if let Some(ticket_str) = ticket {
                println!("\nTicket: {}", ticket_str);
                println!("\nTo connect, run:");
                println!("  hivemind-p2p join <name> --ticket '{}'", ticket_str);
            }
            eprintln!("\nPress Ctrl+C to stop.");
        }
    }
}

/// Display peer connection information
pub fn display_peer_startup(name: &str, use_json: bool, services: &crate::cli::Services) {
    if use_json {
        log_info(&format!("Peer '{}' connected to hub", name), true);
    } else {
        display_box(&format!("Peer '{}' connected to hub", name));
        println!("\nLocal services available at:");
        println!("  Frontend:  http://{}", services.frontend);
        println!("  Backend:   http://{}", services.backend);  
        println!("  WebSocket: ws://{}", services.websocket);
        println!("\nPress Ctrl+C to stop.");
    }
}