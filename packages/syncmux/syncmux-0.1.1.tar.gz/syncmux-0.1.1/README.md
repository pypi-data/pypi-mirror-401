# syncmux

Fast file synchronization for remote development over SSH. syncmux is designed for developers working on remote servers who need low-latency file syncing with persistent connections and robust logging.

## Features

- **🚀 Lightning Fast**: Uses SSH ControlMaster to maintain persistent connections, eliminating handshake overhead for every file.
- **📦 Smart Batching**: Automatically switches to batch mode when multiple files change at once (e.g., switching git branches).
- **🔄 Auto-Reconnect**: Automatically attempts to reconnect if the network drops or the SSH connection is severed.
- **🎯 Git-Aware**: Respects `.gitignore` and logs git diffs for changes.
- **📝 Comprehensive Logging**: Keeps detailed logs of what changed on both the local machine and the remote server.

## Prerequisites

- **Passwordless SSH**: You must have SSH key-based authentication set up for the remote host (e.g., via `ssh-copy-id`), allowing usage without entering a password.
- **rsync**: Must be installed on both the local machine and the remote server.

## Installation

```bash
pip install syncmux
```

## Usage

### Quick Start

Start watching a directory and syncing to a remote server:

```bash
syncmux --local-dir ~/myproject --remote-host dev-server --remote-dir /home/user/myproject
```

### Initial Sync

If you want to ensure the remote directory is an exact mirror of your local directory before starting the watcher (useful for fresh starts), use the `--initial-sync` flag. 

**⚠️ WARNING**: This will delete files on the remote directory that are not present locally.

```bash
syncmux --local-dir ~/myproject --remote-host dev-server --remote-dir /home/user/myproject --initial-sync
```

### Command Line Reference

```text
usage: syncmux [-h] [--version] --local-dir LOCAL_DIR --remote-host REMOTE_HOST
               --remote-dir REMOTE_DIR [--debounce DEBOUNCE]
               [--batch-threshold BATCH_THRESHOLD]
               [--keepalive-interval KEEPALIVE_INTERVAL]
               [--keepalive-count KEEPALIVE_COUNT]
               [--connection-check-interval CONNECTION_CHECK_INTERVAL]
               [--reconnect-attempts RECONNECT_ATTEMPTS]
               [--reconnect-delay RECONNECT_DELAY] [--initial-sync]

Required arguments:
  --local-dir DIR       Local directory to watch
  --remote-host HOST    Remote SSH host (as defined in ~/.ssh/config or user@host)
  --remote-dir DIR      Remote directory path

Sync behavior:
  --debounce SEC        Seconds to wait after last change before syncing (default: 2.0)
  --batch-threshold N   Number of files to trigger batch sync mode (default: 5)

Connection tuning:
  --keepalive-interval N  SSH keepalive interval in seconds (default: 15)
  --reconnect-attempts N  Number of reconnection attempts (default: 5)
```

## How It Works

### Persistent Connection
syncmux sets up a master SSH connection (`ssh -M`) with `ControlPersist`. All subsequent sync operations (`rsync`) reuse this socket. This drastically reduces latency, especially on high-latency networks (like VPNs), as it avoids the SSH handshake overhead for transfer.

### Logging and Diffs
syncmux maintains logs on both ends so you always know what happened.

**Local Log** (`.syncmux-log` in your local dir):
Records every file synced along with the **local git diff** at the time of sync. This allows you to audit exactly what code changes were pushed.

```text
============================================================
Timestamp: 2024-03-20 10:30:01
Synced: src/main.py
Remote: dev-server:/app/src/main.py
----------------------------------------
Diff:
diff --git a/src/main.py b/src/main.py
index ...
...
```

**Remote Log** (`.sync-log` in your remote dir):
Records incoming syncs. If the remote directory is a git repo, it also attempts to capture the diff of the applied changes relative to the remote `HEAD`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to syncmux.

## License

MIT License - see LICENSE file
