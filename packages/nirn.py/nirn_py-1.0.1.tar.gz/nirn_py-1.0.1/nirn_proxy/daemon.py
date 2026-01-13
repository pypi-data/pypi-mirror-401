"""Daemon runner for nirn.py - runs the proxy in the foreground for background process management."""
import os
import sys
from pathlib import Path

# Load .env from the saved working directory or current directory
def load_env():
    """Load environment from .env file."""
    from dotenv import load_dotenv
    
    # Check if there's a saved env path
    if sys.platform == 'win32':
        base = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local'))
    else:
        base = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share'))
    
    env_path_file = base / 'nirn' / 'nirn.env.path'
    
    if env_path_file.exists():
        saved_dir = Path(env_path_file.read_text().strip())
        env_file = saved_dir / '.env'
        if env_file.exists():
            load_dotenv(env_file)
            return
    
    # Fall back to current directory
    load_dotenv()


def main():
    """Run the nirn proxy."""
    # Load environment first
    load_env()
    
    # Import and run the main async function
    from .main import main as run_main
    run_main()


if __name__ == '__main__':
    main()
