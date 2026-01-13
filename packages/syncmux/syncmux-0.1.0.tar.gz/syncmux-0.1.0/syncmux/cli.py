#!/usr/bin/env python3
"""
Command-line interface for syncmux
"""

import sys
import time
import argparse
from pathlib import Path

from .daemon import SyncHandler, setup_ssh_control, cleanup_ssh_control, initial_clean_sync
from .version import __version__

try:
    from watchdog.observers import Observer
except ImportError:
    print("Error: watchdog is not installed. Install it with: pip install watchdog")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog='syncmux',
        description='Fast file synchronization for remote development over SSH',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--version', action='version', version=f'syncmux {__version__}')
    
    # Required arguments
    parser.add_argument('--local-dir', required=True, help='Local directory to watch')
    parser.add_argument('--remote-host', required=True, help='Remote SSH host')
    parser.add_argument('--remote-dir', required=True, help='Remote directory path')
    
    # Optional sync behavior arguments
    parser.add_argument('--debounce', type=float, default=2.0, 
                       help='Seconds to wait after last change before syncing (default: 2.0)')
    parser.add_argument('--batch-threshold', type=int, default=5,
                       help='Number of files to trigger batch sync mode (default: 5)')
    
    # Optional connection arguments
    parser.add_argument('--keepalive-interval', type=int, default=15,
                       help='SSH keepalive interval in seconds (default: 15)')
    parser.add_argument('--keepalive-count', type=int, default=3,
                       help='SSH keepalive max retries (default: 3)')
    parser.add_argument('--connection-check-interval', type=int, default=30,
                       help='Seconds between connection health checks (default: 30)')
    parser.add_argument('--reconnect-attempts', type=int, default=5,
                       help='Number of reconnection attempts (default: 5)')
    parser.add_argument('--reconnect-delay', type=int, default=5,
                       help='Seconds between reconnection attempts (default: 5)')
    
    # Initial sync option
    parser.add_argument('--initial-sync', action='store_true',
                       help='Perform initial clean sync before watching (mirrors source to dest, deletes extra files on dest)')
    
    args = parser.parse_args()
    
    local_dir = Path(args.local_dir).resolve()
    if not local_dir.exists():
        print(f"Error: {local_dir} does not exist")
        sys.exit(1)
    
    print("\n" + "="*60)
    print(f"syncmux v{__version__}")
    print("="*60)
    
    control_path = setup_ssh_control(
        args.remote_host, 
        args.keepalive_interval, 
        args.keepalive_count
    )
    
    config = {
        'debounce_time': args.debounce,
        'batch_threshold': args.batch_threshold,
        'keepalive_interval': args.keepalive_interval,
        'keepalive_count_max': args.keepalive_count,
        'connection_check_interval': args.connection_check_interval,
        'reconnect_attempts': args.reconnect_attempts,
        'reconnect_delay': args.reconnect_delay,
    }
    
    handler = SyncHandler(local_dir, args.remote_host, args.remote_dir, control_path, config)
    
    # Perform initial clean sync if requested (using handler's cached excludes)
    if args.initial_sync:
        print("\n" + "="*60)
        print("Initial Clean Sync Mode")
        print("="*60)
        success = initial_clean_sync(local_dir, args.remote_host, args.remote_dir, control_path, handler.get_rsync_excludes())
        if not success:
            print("\n✗ Initial sync failed. Exiting.")
            cleanup_ssh_control(control_path, args.remote_host)
            sys.exit(1)
        print("\n" + "="*60)
        print("Starting file watcher...")
        print("="*60)
    
    observer = Observer()
    observer.schedule(handler, str(local_dir), recursive=True)
    
    print(f"\n👀 Watching: {local_dir}")
    print(f"📡 Syncing to: {args.remote_host}:{args.remote_dir}")
    print(f"📁 Git repo root: {handler.repo_root}")
    print(f"\n⚙️  Configuration:")
    print(f"   Debounce time: {args.debounce}s")
    print(f"   Batch threshold: {args.batch_threshold} files")
    print(f"   Keepalive interval: {args.keepalive_interval}s")
    print("\nPress Ctrl+C to stop\n")
    print("="*60 + "\n")
    
    observer.start()
    
    try:
        while True:
            time.sleep(0.1)
            handler.process_pending()
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("Stopping...")
        print("="*60)
        observer.stop()
        cleanup_ssh_control(control_path, args.remote_host)
    
    observer.join()
    print("\n✓ syncmux stopped\n")


if __name__ == '__main__':
    main()
