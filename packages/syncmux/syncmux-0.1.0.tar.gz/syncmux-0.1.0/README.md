# syncmux

Fast file synchronization for remote development over SSH.

## Features

- 🚀 Lightning fast with persistent SSH connections
- 📦 Smart batch syncing for bulk operations
- 🔄 Auto-reconnect on network failures  
- 🎯 Git-aware syncing
- 📝 Remote logging with diffs

## Installation

```bash
pip install syncmux
```

## Quick Start

```bash
syncmux --local-dir ~/myproject --remote-host dev-server --remote-dir /home/user/myproject
```

## Usage

```
syncmux \
  --local-dir DIR       Local directory to watch
  --remote-host HOST    Remote SSH host
  --remote-dir DIR      Remote directory path
  
Optional:
  --debounce SECONDS           Wait before syncing (default: 2.0)
  --batch-threshold N          Files for batch mode (default: 5)
  --keepalive-interval N       SSH keepalive (default: 15)
  --reconnect-attempts N       Reconnect tries (default: 5)
```

## How It Works

syncmux uses SSH ControlMaster to maintain a persistent connection. All file syncs reuse this connection, eliminating handshake overhead perfect for high-latency VPN environments.

## License

MIT License - see LICENSE file
