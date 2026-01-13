"""CLI entry point for nirn.py with subcommands."""
import argparse
import os
import sys
import subprocess
import signal
import time
from pathlib import Path


# Default paths for nirn data
def get_nirn_dir() -> Path:
    """Get the nirn data directory."""
    if sys.platform == 'win32':
        base = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local'))
    else:
        base = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share'))
    nirn_dir = base / 'nirn'
    nirn_dir.mkdir(parents=True, exist_ok=True)
    return nirn_dir


def get_pid_file() -> Path:
    """Get the PID file path."""
    return get_nirn_dir() / 'nirn.pid'


def get_log_file() -> Path:
    """Get the log file path."""
    return get_nirn_dir() / 'nirn.log'


def get_env_file() -> Path:
    """Get the saved env directory file path."""
    return get_nirn_dir() / 'nirn.env.path'


def is_running() -> tuple[bool, int | None]:
    """Check if nirn is currently running."""
    pid_file = get_pid_file()
    if not pid_file.exists():
        return False, None
    
    try:
        pid = int(pid_file.read_text().strip())
    except (ValueError, IOError):
        return False, None
    
    # Check if process is actually running
    if sys.platform == 'win32':
        try:
            # Use tasklist to check if PID exists
            result = subprocess.run(
                ['tasklist', '/FI', f'PID eq {pid}', '/NH'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if str(pid) in result.stdout:
                return True, pid
        except Exception:
            pass
    else:
        try:
            os.kill(pid, 0)
            return True, pid
        except OSError:
            pass
    
    # Process not running, clean up stale PID file
    pid_file.unlink(missing_ok=True)
    return False, None


def cmd_start(args):
    """Start nirn as a background process."""
    running, pid = is_running()
    if running:
        print(f"nirn is already running (PID: {pid})")
        print(f"Use 'nirn stop' to stop it first, or 'nirn logs' to view logs")
        return 1
    
    # Get the current working directory for .env loading
    cwd = Path.cwd()
    
    # Save the working directory so we can reference it
    env_path_file = get_env_file()
    env_path_file.write_text(str(cwd))
    
    log_file = get_log_file()
    pid_file = get_pid_file()
    
    # Find the Python executable
    python_exe = sys.executable
    
    # Build the command to run nirn
    # We'll use a wrapper script approach
    cmd = [python_exe, '-m', 'nirn_proxy.daemon']
    
    print(f"Starting nirn...")
    print(f"  Working directory: {cwd}")
    print(f"  Log file: {log_file}")
    
    try:
        if sys.platform == 'win32':
            # On Windows, use CREATE_NEW_PROCESS_GROUP and DETACHED_PROCESS
            DETACHED_PROCESS = 0x00000008
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            CREATE_NO_WINDOW = 0x08000000
            
            with open(log_file, 'a') as log_out:
                process = subprocess.Popen(
                    cmd,
                    cwd=str(cwd),
                    stdout=log_out,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW,
                    start_new_session=True
                )
        else:
            # On Unix, use nohup-like behavior
            with open(log_file, 'a') as log_out:
                process = subprocess.Popen(
                    cmd,
                    cwd=str(cwd),
                    stdout=log_out,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True
                )
        
        # Write PID file
        pid_file.write_text(str(process.pid))
        
        # Wait a moment and check if it started successfully
        time.sleep(1.5)
        
        running, _ = is_running()
        if running:
            print(f"nirn started successfully (PID: {process.pid})")
            print(f"\nUseful commands:")
            print(f"  nirn logs          - View logs")
            print(f"  nirn logs --lines=50  - View last 50 lines")
            print(f"  nirn stop          - Stop nirn")
            return 0
        else:
            print("nirn failed to start. Check logs with 'nirn logs'")
            return 1
            
    except Exception as e:
        print(f"Failed to start nirn: {e}")
        return 1


def cmd_stop(args):
    """Stop nirn."""
    running, pid = is_running()
    if not running:
        print("nirn is not running")
        return 0
    
    print(f"Stopping nirn (PID: {pid})...")
    
    try:
        if sys.platform == 'win32':
            # On Windows, use taskkill
            subprocess.run(
                ['taskkill', '/PID', str(pid), '/F'],
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            # On Unix, send SIGTERM
            os.kill(pid, signal.SIGTERM)
            
            # Wait for graceful shutdown
            for _ in range(10):
                time.sleep(0.5)
                try:
                    os.kill(pid, 0)
                except OSError:
                    break
            else:
                # Force kill if still running
                try:
                    os.kill(pid, signal.SIGKILL)
                except OSError:
                    pass
        
        # Clean up PID file
        get_pid_file().unlink(missing_ok=True)
        
        print("nirn stopped")
        return 0
        
    except Exception as e:
        print(f"Failed to stop nirn: {e}")
        return 1


def cmd_logs(args):
    """Show nirn logs."""
    log_file = get_log_file()
    
    if not log_file.exists():
        print("No log file found. Is nirn running?")
        print(f"Expected log file at: {log_file}")
        return 1
    
    lines = args.lines
    
    try:
        with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
            if lines == 0:
                # Show all logs
                content = f.read()
            else:
                # Read last N lines efficiently
                # Seek to end and read backwards
                f.seek(0, 2)  # Seek to end
                file_size = f.tell()
                
                if file_size == 0:
                    print("Log file is empty")
                    return 0
                
                # Read in chunks from the end
                chunk_size = 8192
                found_lines = []
                remaining = file_size
                
                while len(found_lines) <= lines and remaining > 0:
                    chunk_start = max(0, remaining - chunk_size)
                    f.seek(chunk_start)
                    chunk = f.read(remaining - chunk_start)
                    remaining = chunk_start
                    
                    chunk_lines = chunk.splitlines(keepends=True)
                    
                    # If we didn't start at beginning, first line might be partial
                    if remaining > 0 and found_lines:
                        # Prepend to first found line
                        found_lines[0] = chunk_lines[-1] + found_lines[0]
                        chunk_lines = chunk_lines[:-1]
                    
                    found_lines = chunk_lines + found_lines
                
                # Take only the last N lines
                content = ''.join(found_lines[-lines:])
        
        if content:
            print(content, end='' if content.endswith('\n') else '\n')
        else:
            print("Log file is empty")
            
        return 0
        
    except Exception as e:
        print(f"Failed to read logs: {e}")
        return 1


def cmd_status(args):
    """Show nirn status."""
    running, pid = is_running()
    
    print("nirn status:")
    if running:
        print(f"  Status: Running (PID: {pid})")
    else:
        print("  Status: Stopped")
    
    log_file = get_log_file()
    print(f"  Log file: {log_file}")
    if log_file.exists():
        size = log_file.stat().st_size
        if size < 1024:
            print(f"  Log size: {size} bytes")
        elif size < 1024 * 1024:
            print(f"  Log size: {size / 1024:.1f} KB")
        else:
            print(f"  Log size: {size / (1024 * 1024):.1f} MB")
    
    env_file = get_env_file()
    if env_file.exists():
        print(f"  Working dir: {env_file.read_text().strip()}")
    
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='nirn',
        description='nirn.py - Discord API rate limit proxy',
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # start command
    start_parser = subparsers.add_parser(
        'start',
        help='Start nirn as a background process'
    )
    start_parser.set_defaults(func=cmd_start)
    
    # stop command
    stop_parser = subparsers.add_parser(
        'stop',
        help='Stop nirn'
    )
    stop_parser.set_defaults(func=cmd_stop)
    
    # logs command
    logs_parser = subparsers.add_parser(
        'logs',
        help='View nirn logs'
    )
    logs_parser.add_argument(
        '--lines', '-n',
        type=int,
        default=50,
        help='Number of lines to show (default: 50, use 0 for all)'
    )
    logs_parser.set_defaults(func=cmd_logs)
    
    # status command
    status_parser = subparsers.add_parser(
        'status',
        help='Show nirn status'
    )
    status_parser.set_defaults(func=cmd_status)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
