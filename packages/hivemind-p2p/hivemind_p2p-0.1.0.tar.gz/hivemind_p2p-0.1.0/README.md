# Hivemind P2P

A peer-to-peer port forwarding system for sharing three Hivemind services (frontend, backend, websocket) over encrypted QUIC connections using [iroh](https://iroh.computer/).

## Features

- **Zero-configuration P2P**: Connect directly using tickets or join codes, no VPN or port forwarding needed
- **Hub-and-peer architecture**: One hub shares services to multiple peers
- **Magic Wormhole integration**: User-friendly join codes (e.g., "5-hamburger-endorse") via Magic Wormhole
- **Three-port forwarding**: Frontend, backend, and websocket services over a single connection
- **Encrypted transport**: All traffic encrypted via QUIC with iroh
- **NAT traversal**: Built-in relay fallback for difficult network configurations
- **Lazy stream creation**: Efficient on-demand stream allocation per TCP connection
- **Graceful shutdown**: Clean Ctrl+C handling on both hub and peer

## Installation

### Option 1: Python Wheel (Recommended)

The easiest way to install is via the Python wheel, which bundles the pre-built binary.

**Prerequisites:**
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

```bash
# Install with uv
uv pip install hivemind-p2p

# Or with pip
pip install hivemind-p2p
```

### Option 2: Build from Source (Rust)

**Prerequisites:**
- Rust 1.70 or later
- Cargo

```bash
git clone https://github.com/your-org/hivemind-p2p.git
cd hivemind-p2p
cargo build --release
```

The binary will be available at `target/release/hivemind-p2p`.

### Option 3: Build Python Wheel Locally

Build the Python wheel from source using maturin:

**Prerequisites:**
- Rust 1.70+
- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

```bash
# Create virtual environment and install dev dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install maturin

# Build the wheel (development mode - editable install)
uv run python -m maturin develop --release

# Or build a distributable wheel
maturin build --release
# Wheel will be in target/wheels/
```

## Quick Start

### Hub Mode (Share Services)

Start a hub to share three local services:

```bash
# Share services running on localhost
hivemind-p2p share 127.0.0.1:3000 127.0.0.1:8000 127.0.0.1:4000 my-hub
```

The hub will display a ticket string like:
```
╔══════════════════════════════════════════════════════════════════════════════╗
║ Hub 'my-hub' is running                                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

Ticket: nodeaddrwhatever...

To connect, run:
  hivemind-p2p join <name> --ticket 'nodeaddrwhatever...'
```

### Hub Mode with Magic Wormhole (Easy Join Codes)

Use Magic Wormhole to generate easy-to-share join codes:

```bash
# Share with wormhole mode (generates rotating join codes)
hivemind-p2p share 127.0.0.1:3000 127.0.0.1:8000 127.0.0.1:4000 my-hub --wormhole
```

Output:
```
╔══════════════════════════════════════════════════════════════════════════════╗
║ Hub 'my-hub' starting with Magic Wormhole                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────────┐
│  Join code: 5-hamburger-endorse        │
└────────────────────────────────────────┘
Waiting for peer to connect...
```

### Peer Mode (Join a Hub)

#### Using Direct Ticket

```bash
# Join using ticket string
hivemind-p2p join my-peer --ticket 'nodeaddrwhatever...'
```

#### Using Magic Wormhole Join Code

```bash
# Join using wormhole code (much easier!)
hivemind-p2p join my-peer --join-code 5-hamburger-endorse
```

The peer will connect and expose services locally:
```
╔══════════════════════════════════════════════════════════════════════════════╗
║ Peer 'my-peer' connected to hub                                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Local services available at:
  Frontend:  http://127.0.0.1:3000
  Backend:   http://127.0.0.1:8000
  WebSocket: ws://127.0.0.1:4000

Press Ctrl+C to stop.
```

## Usage Examples

### Example 1: Share a Web Application

```bash
# Terminal 1: Start your web app
cd my-web-app
npm run dev  # Frontend on :3000, Backend on :8000, WebSocket on :4000

# Terminal 2: Share it via P2P hub
hivemind-p2p share 127.0.0.1:3000 127.0.0.1:8000 127.0.0.1:4000 dev-server --wormhole

# Terminal 3 (remote machine): Connect and access
hivemind-p2p join remote-dev --join-code 5-hamburger-endorse
# Now access http://127.0.0.1:3000 on the remote machine
```

### Example 2: Custom Ports for Peer

```bash
# Join with custom local ports
hivemind-p2p join my-peer \
  --join-code 5-hamburger-endorse \
  --frontend-addr 127.0.0.1:3001 \
  --backend-addr 127.0.0.1:8001 \
  --ws-addr 127.0.0.1:4001
```

### Example 3: Using Custom Relay Server

```bash
# Hub with custom Magic Wormhole relay
hivemind-p2p share 127.0.0.1:3000 127.0.0.1:8000 127.0.0.1:4000 my-hub \
  --wormhole \
  --wormhole-relay https://my-relay.example.com

# Peer with matching relay
hivemind-p2p join my-peer \
  --join-code 5-hamburger-endorse \
  --wormhole-relay https://my-relay.example.com
```

### Example 4: Verbose Logging

```bash
# Different verbosity levels
hivemind-p2p share ... my-hub --wormhole -v    # Warnings
hivemind-p2p share ... my-hub --wormhole -vv   # Info
hivemind-p2p share ... my-hub --wormhole -vvv  # Debug
hivemind-p2p share ... my-hub --wormhole -vvvv # Trace
```

## Architecture

### Hub-and-Peer Model

```
           Hub (shares services)
              /    |    \
             /     |     \
            /      |      \
      Peer 1   Peer 2   Peer 3
   (accesses)  (accesses) (accesses)
```

### Protocol Design

1. **Connection Layer**: QUIC encrypted transport via iroh
2. **Bootstrap Layer**: Magic Wormhole for initial ticket exchange (optional)
3. **Handshake Protocol**:
   - Peer sends: `[PORT_ID][HANDSHAKE("hivemindp2p")]`
   - Hub responds: `[ACK_SUCCESS]` or `[ACK_ERROR]`
4. **Data Layer**: Bidirectional TCP↔QUIC forwarding

### Port IDs

- `0x01`: Frontend service (default: 3000)
- `0x02`: Backend service (default: 8000)
- `0x03`: WebSocket service (default: 4000)

### Stream Lifecycle

- **Lazy Creation**: Streams are created on-demand when TCP connections arrive
- **Multiplexing**: Multiple TCP connections can share the same QUIC connection
- **Bidirectional**: Each stream forwards data in both directions concurrently
- **Graceful Cleanup**: Streams clean up when either direction completes

## CLI Reference

### Global Options

```
--alpn <TYPE>                ALPN protocol (hivemind|federated-hivemind) [default: hivemind]
--ipv4-addr <ADDR>          IPv4 bind address (e.g., 0.0.0.0:8080)
--ipv6-addr <ADDR>          IPv6 bind address
-v, --verbose               Increase verbosity (repeat for more: -vvv)
--wormhole-relay <URL>      Custom Magic Wormhole relay server
```

### Share Command

```bash
hivemind-p2p share <FRONTEND> <BACKEND> <WEBSOCKET> <NAME> [OPTIONS]

Arguments:
  <FRONTEND>    Address of frontend service (e.g., 127.0.0.1:3000)
  <BACKEND>     Address of backend service (e.g., 127.0.0.1:8000)
  <WEBSOCKET>   Address of websocket service (e.g., 127.0.0.1:4000)
  <NAME>        Name for this hub

Options:
  --wormhole    Use Magic Wormhole for easy join codes
```

### Join Command

```bash
hivemind-p2p join <NAME> [OPTIONS]

Arguments:
  <NAME>        Name for this peer

Options:
  --ticket <TICKET>              EndpointTicket string from hub
  --join-code <CODE>             Magic Wormhole code (e.g., "5-hamburger-endorse")
  --frontend-addr <ADDR>         Local address for frontend [default: 127.0.0.1:3000]
  --backend-addr <ADDR>          Local address for backend [default: 127.0.0.1:8000]
  --ws-addr <ADDR>               Local address for websocket [default: 127.0.0.1:4000]

Note: Either --ticket or --join-code must be provided (mutually exclusive)
```

## Testing

### Rust Tests

```bash
# Run all tests (except network-dependent ones)
cargo test

# Run all tests including network tests
cargo test -- --include-ignored

# Run specific test suite
cargo test --test cli_tests
cargo test --test ticket_tests
cargo test --test e2e_http_test

# Run with output visible
cargo test -- --nocapture
```

### Python Wheel Tests

Test the Python wheel installation and binary locator:

```bash
cd hivemind-p2p

# Setup with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync --dev

# Build the wheel (includes Rust binary)
maturin build --release

# Install the wheel with pip (not uv pip, which uses editable mode)
python -m pip install target/wheels/hivemind_p2p-*.whl --force-reinstall

# Verify installation
hivemind-p2p --help
python -c "from hivemind_p2p import get_binary_path; print(get_binary_path())"

# Run Python tests
.venv/bin/pytest tests/test_binary.py -v
```

**Note:** Use `python -m pip install` instead of `uv pip install` because uv treats local wheel files as editable installs, which doesn't properly install the bundled binary script.

The Python tests verify:
- Binary is correctly located after installation
- Binary is executable
- `--help` commands work for share/join subcommands

### Test Coverage

- **Unit Tests** (4): Protocol constants, ALPN types
- **CLI Tests** (4): Argument parsing and validation
- **Integration Tests** (2): Ticket roundtrip, wormhole flow
- **E2E Tests** (1): Complete handshake protocol

### Manual E2E Testing

```bash
# Terminal 1: Start test HTTP server
python3 -m http.server 3000 &
python3 -m http.server 8000 &
python3 -m http.server 4000 &

# Terminal 2: Start hub
cargo run -- share 127.0.0.1:3000 127.0.0.1:8000 127.0.0.1:4000 test-hub

# Terminal 3: Join as peer
cargo run -- join test-peer --ticket '<ticket-from-terminal-2>'

# Terminal 4: Test connection
curl http://127.0.0.1:3000
```

## Troubleshooting

### Connection Issues

**Problem**: Peer can't connect to hub

**Solutions**:
- Verify the ticket/join code is correct and hasn't expired (wormhole codes are ephemeral)
- Check network connectivity - try with `-vv` for debug logs
- Ensure firewall rules allow QUIC traffic (UDP)
- Hub and peer should use matching `--wormhole-relay` if custom relay is used

### Port Already in Use

**Problem**: `Address already in use` error

**Solutions**:
- Use different ports with `--frontend-addr`, `--backend-addr`, `--ws-addr`
- Check if services are already running: `lsof -i :3000`
- Kill existing processes or choose different ports

### Slow Initial Connection

**Problem**: First connection takes 5-10 seconds

**Explanation**: This is normal - iroh is performing NAT traversal and may fall back to relay servers. Subsequent connections will be faster.

### Magic Wormhole Connection Failed

**Problem**: `Failed to connect to wormhole server`

**Solutions**:
- Check internet connectivity
- Try using a custom relay with `--wormhole-relay`
- Fall back to direct ticket mode (without `--wormhole`)

### Services Not Forwarding Data

**Problem**: Connection established but no data flows

**Solutions**:
- Verify the hub services are actually running on the specified ports
- Check logs with `-vvv` for forwarding errors
- Ensure the peer is connecting to the correct local ports
- Test the hub services locally first: `curl http://127.0.0.1:3000`

## Development

### Project Structure

```
hivemind-p2p/
├── src/
│   ├── main.rs         # CLI entry point, hub/peer handlers
│   ├── lib.rs          # Constants, protocol definitions
│   ├── cli.rs          # Clap argument parsing
│   ├── peer.rs         # Bidirectional TCP↔QUIC forwarding
│   └── wormhole.rs     # Magic Wormhole integration
├── tests/
│   ├── cli_tests.rs        # CLI argument tests
│   ├── ticket_tests.rs     # Ticket roundtrip tests
│   ├── wormhole_tests.rs   # Wormhole integration tests
│   └── e2e_http_test.rs    # End-to-end handshake test
├── Cargo.toml
├── README.md
└── CLAUDE.md          # Developer documentation
```

### Code Quality

```bash
# Run linter
cargo clippy

# Format code
cargo fmt

# Check formatting
cargo fmt --check

# Build in release mode
cargo build --release
```

### Releasing

To publish a new release to PyPI:

1. Update version in `Cargo.toml`, `pyproject.toml`, and `python/hivemind_p2p/__init__.py`
2. Commit and tag:
   ```bash
   git commit -am "Release v0.1.0"
   git tag v0.1.0
   git push origin main --tags
   ```
3. GitHub Actions will automatically build wheels for all platforms and publish to PyPI

**First-time setup:** Configure [PyPI trusted publisher](https://docs.pypi.org/trusted-publishers/) for the repository.

## Dependencies

### Core Dependencies

- **iroh** (0.95): P2P networking, QUIC transport, NAT traversal
- **iroh-tickets** (0.2): Compact endpoint ticket serialization
- **magic-wormhole** (0.7.6): User-friendly join code exchange
- **tokio**: Async runtime
- **clap**: CLI argument parsing
- **tracing**: Structured logging

### Development Dependencies

- **tokio-test**: Async test utilities
- **axum**: HTTP server for E2E tests
- **tower**: Service middleware
- **hyper**: HTTP client for tests