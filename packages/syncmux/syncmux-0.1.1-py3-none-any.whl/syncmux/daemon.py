#!/usr/bin/env python3
"""
syncmux.daemon - Core sync daemon functionality
"""

import os
import sys
import time
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime

try:
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Error: watchdog is not installed. Install it with: pip install watchdog")
    sys.exit(1)


class SyncHandler(FileSystemEventHandler):
    def __init__(self, local_dir, remote_host, remote_dir, ssh_control, config):
        self.local_dir = Path(local_dir).resolve()
        self.remote_host = remote_host
        self.remote_dir = remote_dir
        self.ssh_control = ssh_control
        self.file_hashes = {}
        
        # Configuration (with defaults)
        self.debounce_time = config.get('debounce_time', 2.0)
        self.batch_threshold = config.get('batch_threshold', 5)
        self.connection_check_interval = config.get('connection_check_interval', 30)
        self.keepalive_interval = config.get('keepalive_interval', 15)
        self.keepalive_count_max = config.get('keepalive_count_max', 3)
        self.reconnect_attempts = config.get('reconnect_attempts', 5)
        self.reconnect_delay = config.get('reconnect_delay', 5)
        
        self.pending_syncs = {}
        self.repo_root = self.find_git_root()
        self.connection_failed = False
        self.last_connection_check = 0
        
        # Local sync log file
        self.local_log_file = self.local_dir / '.syncmux-log'
        
        # Cache rsync excludes (read .gitignore once)
        self._rsync_excludes = self._build_rsync_excludes()
    
    def _build_rsync_excludes(self):
        """Build rsync exclude arguments from .gitignore plus default excludes (called once)"""
        excludes = []
        
        # Always exclude these directories
        always_exclude = ['.git', '.cache', '.syncmux-log']
        for pattern in always_exclude:
            excludes.extend(['--exclude', pattern])
        
        # Read .gitignore if it exists
        gitignore_path = self.repo_root / '.gitignore'
        if gitignore_path.exists():
            try:
                with open(gitignore_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        # Skip empty lines and comments
                        if line and not line.startswith('#'):
                            # Handle negation patterns (rsync doesn't support ! the same way)
                            if line.startswith('!'):
                                continue
                            excludes.extend(['--exclude', line])
            except Exception as e:
                print(f"⚠️  Could not read .gitignore: {e}")
        
        return excludes
    
    def get_timestamp(self):
        """Get current timestamp in readable format"""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def get_file_diff(self, filepath):
        """Get git diff for a file if in a git repo"""
        try:
            result = subprocess.run(
                ['git', 'diff', 'HEAD', '--', str(filepath)],
                cwd=str(self.repo_root),
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            else:
                # Check if it's a new file (untracked)
                status_result = subprocess.run(
                    ['git', 'status', '--porcelain', str(filepath)],
                    cwd=str(self.repo_root),
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if status_result.stdout.startswith('??'):
                    return '[New untracked file]'
                elif status_result.stdout.startswith('A'):
                    return '[Newly added file]'
                return '[No changes detected or binary file]'
        except Exception as e:
            return f'[Could not get diff: {e}]'
    
    def log_sync_local(self, filepath, is_batch=False, batch_files=None):
        """Log sync operation to local log file with diff"""
        timestamp = self.get_timestamp()
        
        try:
            with open(self.local_log_file, 'a') as f:
                f.write("=" * 60 + "\n")
                f.write(f"Timestamp: {timestamp}\n")
                
                if is_batch and batch_files:
                    f.write(f"Batch sync: {len(batch_files)} files\n")
                    f.write(f"Remote: {self.remote_host}:{self.remote_dir}\n")
                    f.write("-" * 40 + "\n")
                    for fp in batch_files:
                        rel_path = fp.relative_to(self.local_dir)
                        f.write(f"\nFile: {rel_path}\n")
                        diff = self.get_file_diff(fp)
                        f.write(f"Diff:\n{diff}\n")
                else:
                    rel_path = filepath.relative_to(self.local_dir)
                    f.write(f"Synced: {rel_path}\n")
                    f.write(f"Remote: {self.remote_host}:{self.remote_dir}/{rel_path}\n")
                    f.write("-" * 40 + "\n")
                    diff = self.get_file_diff(filepath)
                    f.write(f"Diff:\n{diff}\n")
                
                f.write("\n")
        except Exception as e:
            print(f"⚠️  Could not write to local log: {e}")
    
    def get_rsync_excludes(self):
        """Return cached rsync exclude arguments"""
        return self._rsync_excludes
    
    def find_git_root(self):
        """Find the git repository root"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--show-toplevel'],
                cwd=str(self.local_dir),
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return Path(result.stdout.strip())
        except:
            pass
        return self.local_dir
    
    def get_file_hash(self, filepath):
        """Quick hash to detect actual changes"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def check_connection(self):
        """Check if SSH connection is still alive"""
        try:
            result = subprocess.run(
                ['ssh', '-O', 'check', '-o', f'ControlPath={self.ssh_control}', self.remote_host],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def reconnect(self):
        """Attempt to reconnect SSH ControlMaster"""
        print("\n⚠️  Connection lost, attempting to reconnect...")
        
        subprocess.run(
            ['ssh', '-O', 'exit', '-o', f'ControlPath={self.ssh_control}', self.remote_host],
            capture_output=True
        )
        
        for attempt in range(1, self.reconnect_attempts + 1):
            print(f"   Attempt {attempt}/{self.reconnect_attempts}...")
            
            cmd = [
                'ssh', '-fNM',
                '-o', f'ControlPath={self.ssh_control}',
                '-o', 'ControlPersist=yes',
                '-o', f'ServerAliveInterval={self.keepalive_interval}',
                '-o', f'ServerAliveCountMax={self.keepalive_count_max}',
                '-o', 'TCPKeepAlive=yes',
                self.remote_host
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✓ Reconnected successfully!")
                self.connection_failed = False
                return True
            
            time.sleep(self.reconnect_delay)
        
        print(f"✗ Failed to reconnect after {self.reconnect_attempts} attempts")
        self.connection_failed = True
        return False
    
    def ensure_connection(self):
        """Ensure connection is alive, reconnect if needed"""
        now = time.time()
        
        if self.connection_failed or (now - self.last_connection_check > self.connection_check_interval):
            self.last_connection_check = now
            
            if not self.check_connection():
                return self.reconnect()
        
        return True
    
    def sync_batch(self, filepaths):
        """Sync multiple files at once using a single rsync command"""
        if not filepaths:
            return
        
        if not self.ensure_connection():
            print(f"✗ Cannot sync {len(filepaths)} files - no connection")
            for fp in filepaths:
                self.pending_syncs[fp] = time.time()
            return False
        
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            for filepath in filepaths:
                rel_path = filepath.relative_to(self.local_dir)
                f.write(f"{rel_path}\n")
            files_list = f.name
        
        try:
            cmd = [
                'rsync', '-az',
                '--files-from', files_list,
                '-e', f'ssh -o ControlPath={self.ssh_control}',
            ]
            # Add excludes from .gitignore + defaults
            cmd.extend(self.get_rsync_excludes())
            cmd.extend([
                str(self.local_dir) + '/',
                f"{self.remote_host}:{self.remote_dir}/"
            ])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                timestamp = self.get_timestamp()
                print(f"[{timestamp}] ✓ Batch synced {len(filepaths)} files")
                
                # Log to local file
                self.log_sync_local(None, is_batch=True, batch_files=filepaths)
                
                file_list = ', '.join([str(fp.relative_to(self.local_dir)) for fp in filepaths[:5]])
                if len(filepaths) > 5:
                    file_list += f" and {len(filepaths) - 5} more"
                
                log_script = f'''cd {self.remote_dir} && {{
                    echo "========================================" >> .sync-log
                    echo "$(date '+%Y-%m-%d %H:%M:%S') - Batch synced {len(filepaths)} files" >> .sync-log
                    echo "  Files: {file_list}" >> .sync-log
                    echo "" >> .sync-log
                }}'''
                
                log_cmd = f"ssh -o ControlPath={self.ssh_control} {self.remote_host} '{log_script}'"
                subprocess.run(log_cmd, capture_output=True, timeout=5, shell=True, text=True)
                
                return True
            else:
                print(f"✗ Batch sync failed: {result.stderr}")
                if "Connection" in result.stderr or "refused" in result.stderr:
                    self.connection_failed = True
                return False
                
        except subprocess.TimeoutExpired:
            print(f"✗ Batch sync timeout - connection may be lost")
            self.connection_failed = True
            for fp in filepaths:
                self.pending_syncs[fp] = time.time()
            return False
        except Exception as e:
            print(f"✗ Batch sync error: {e}")
            return False
        finally:
            try:
                os.unlink(files_list)
            except:
                pass
    
    def sync_file(self, filepath):
        """Send file to remote via rsync over persistent SSH"""
        if not self.ensure_connection():
            print(f"✗ Cannot sync - no connection")
            self.pending_syncs[filepath] = time.time()
            return False
        
        rel_path = filepath.relative_to(self.local_dir)
        remote_path = f"{self.remote_host}:{self.remote_dir}/{rel_path}"
        
        try:
            cmd = [
                'rsync', '-az',
                '-e', f'ssh -o ControlPath={self.ssh_control}',
            ]
            # Add excludes from .gitignore + defaults
            cmd.extend(self.get_rsync_excludes())
            cmd.extend([
                str(filepath),
                remote_path
            ])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                timestamp = self.get_timestamp()
                print(f"[{timestamp}] ✓ Synced: {rel_path}")
                
                # Log to local file
                self.log_sync_local(filepath)
                
                log_script = f'''cd {self.remote_dir} && {{
                    echo "========================================" >> .sync-log
                    echo "$(date '+%Y-%m-%d %H:%M:%S') - Synced: {rel_path}" >> .sync-log
                    if git rev-parse --git-dir > /dev/null 2>&1; then
                        echo "Diff:" >> .sync-log
                        git diff HEAD {rel_path} >> .sync-log 2>/dev/null || echo "  (New file or binary)" >> .sync-log
                    else
                        echo "  (git not available for diff)" >> .sync-log
                    fi
                    echo "" >> .sync-log
                }}'''
                
                log_cmd = f"ssh -o ControlPath={self.ssh_control} {self.remote_host} '{log_script}'"
                subprocess.run(log_cmd, capture_output=True, timeout=5, shell=True, text=True)
                
                return True
            else:
                print(f"✗ Failed to sync {rel_path}: {result.stderr}")
                if "Connection" in result.stderr or "refused" in result.stderr:
                    self.connection_failed = True
                return False
                
        except subprocess.TimeoutExpired:
            print(f"✗ Timeout syncing {rel_path} - connection may be lost")
            self.connection_failed = True
            self.pending_syncs[filepath] = time.time()
            return False
        except Exception as e:
            print(f"✗ Error syncing {rel_path}: {e}")
            return False
    
    def should_sync(self, filepath):
        """Check if file should be synced"""
        pause_file = self.repo_root / '.sync-pause'
        if pause_file.exists():
            return False
        
        parts = filepath.parts
        skip_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.DS_Store'}
        skip_exts = {'.pyc', '.swp', '.swo', '.swn', '.tmp'}
        
        if any(d in parts for d in skip_dirs):
            return False
        
        if filepath.suffix in skip_exts:
            return False
            
        return True
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        filepath = Path(event.src_path)
        
        if not self.should_sync(filepath):
            return
        
        current_hash = self.get_file_hash(filepath)
        if current_hash is None:
            return
            
        if filepath in self.file_hashes and self.file_hashes[filepath] == current_hash:
            return
        
        self.file_hashes[filepath] = current_hash
        self.pending_syncs[filepath] = time.time()
        
    def on_created(self, event):
        self.on_modified(event)
    
    def process_pending(self):
        """Process pending syncs after debounce period"""
        now = time.time()
        to_sync = []
        
        for filepath, timestamp in list(self.pending_syncs.items()):
            if now - timestamp >= self.debounce_time:
                to_sync.append(filepath)
                del self.pending_syncs[filepath]
        
        if not to_sync:
            return
        
        if len(to_sync) >= self.batch_threshold:
            print(f"📦 Detected bulk operation ({len(to_sync)} files), using batch sync...")
            self.sync_batch(to_sync)
        else:
            for filepath in to_sync:
                self.sync_file(filepath)


def setup_ssh_control(remote_host, keepalive_interval=15, keepalive_count_max=3):
    """Setup SSH ControlMaster for persistent connection with keepalive"""
    control_path = Path.home() / '.ssh' / f'control-sync-{remote_host}'
    
    print(f"Setting up SSH ControlMaster to {remote_host}...")
    
    cmd = [
        'ssh', '-fNM',
        '-o', f'ControlPath={control_path}',
        '-o', 'ControlPersist=yes',
        '-o', f'ServerAliveInterval={keepalive_interval}',
        '-o', f'ServerAliveCountMax={keepalive_count_max}',
        '-o', 'TCPKeepAlive=yes',
        remote_host
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Failed to establish SSH connection: {result.stderr}")
        sys.exit(1)
    
    print(f"✓ SSH ControlMaster established")
    print(f"✓ Keepalive enabled ({keepalive_interval}s interval)")
    return str(control_path)


def cleanup_ssh_control(control_path, remote_host):
    """Close SSH ControlMaster"""
    print("\nClosing SSH connection...")
    subprocess.run([
        'ssh', '-O', 'exit', 
        '-o', f'ControlPath={control_path}',
        remote_host
    ], capture_output=True)
    print("✓ Connection closed")


def initial_clean_sync(local_dir, remote_host, remote_dir, control_path, rsync_excludes):
    """
    Perform initial clean sync from source to destination.
    Creates an exact mirror copy, deleting any extra files on destination.
    """
    local_dir = Path(local_dir).resolve()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"\n[{timestamp}] 🔄 Starting initial clean sync...")
    print(f"   Source: {local_dir}")
    print(f"   Destination: {remote_host}:{remote_dir}")
    print(f"\n⚠️  WARNING: This will DELETE any files on destination that don't exist in source!")
    
    # Build rsync command with --delete for exact mirroring
    cmd = [
        'rsync', '-avz', '--delete', '--progress',
        '-e', f'ssh -o ControlPath={control_path}',
    ]
    cmd.extend(rsync_excludes)
    cmd.extend([
        str(local_dir) + '/',
        f"{remote_host}:{remote_dir}/"
    ])
    
    try:
        print(f"\n{'='*60}")
        result = subprocess.run(cmd, text=True, timeout=300)
        print(f"{'='*60}\n")
        
        if result.returncode == 0:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] ✓ Initial clean sync completed successfully!")
            
            # Log to local file
            log_file = local_dir / '.syncmux-log'
            try:
                with open(log_file, 'a') as f:
                    f.write("=" * 60 + "\n")
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"INITIAL CLEAN SYNC\n")
                    f.write(f"Source: {local_dir}\n")
                    f.write(f"Destination: {remote_host}:{remote_dir}\n")
                    f.write(f"Status: SUCCESS\n")
                    f.write("\n")
            except Exception as e:
                print(f"⚠️  Could not write to local log: {e}")
            
            return True
        else:
            print(f"✗ Initial sync failed with return code: {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ Initial sync timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"✗ Initial sync error: {e}")
        return False
