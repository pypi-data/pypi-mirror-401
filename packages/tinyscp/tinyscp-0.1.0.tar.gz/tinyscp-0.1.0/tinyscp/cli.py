"""
TinySCP Command Line Interface
"""

import os
import sys
import signal
import argparse
import logging

from .server import TinySCPServer

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file"""
    defaults = {
        'host': '0.0.0.0',
        'port': 2222,
        'host_key': './tinyscp_host_key',
        'upload_dir': './uploads',
        'download_dir': './downloads',
        'users': {}
    }
    
    if config_path and os.path.exists(config_path):
        if not HAS_YAML:
            print("WARNING: PyYAML not installed, using defaults. Install with: pip install pyyaml")
            return defaults
        
        with open(config_path, 'r') as f:
            file_config = yaml.safe_load(f) or {}
        defaults.update(file_config)
    
    return defaults


def save_default_config(config_path: str) -> None:
    """Save a default configuration file"""
    if not HAS_YAML:
        print("ERROR: PyYAML required to generate config. Install with: pip install pyyaml")
        sys.exit(1)
    
    default = {
        'host': '0.0.0.0',
        'port': 2222,
        'host_key': './tinyscp_host_key',
        'upload_dir': './uploads',
        'download_dir': './downloads',
        'users': {
            'admin': 'changeme',
            'neteng': 'firmware123'
        }
    }
    
    with open(config_path, 'w') as f:
        yaml.dump(default, f, default_flow_style=False)
    
    print(f"Created default config: {config_path}")
    print("Edit the file to set your users and passwords.")


def setup_logging(debug: bool = False) -> None:
    """Configure logging"""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' if debug else '%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main() -> None:
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='TinySCP - Simple Bidirectional SCP Server',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tinyscp                            # Run with defaults (looks for config.yaml)
  tinyscp -c myconfig.yaml           # Use specific config file
  tinyscp --init-config config.yaml  # Generate default config
  tinyscp -d -p 2222                 # Debug mode on port 2222
  tinyscp --no-config -p 2222 -u admin:secret  # CLI-only mode

Client usage (remember -O for legacy SCP mode on modern systems):
  Upload:   scp -O -P 2222 file.bin user@host:/uploads/
  Download: scp -O -P 2222 user@host:/downloads/file.bin ./
        """
    )
    parser.add_argument('-d', '--debug', action='store_true', 
                        help='Enable debug output')
    parser.add_argument('-p', '--port', type=int, 
                        help='Port to listen on (default: 2222)')
    parser.add_argument('-H', '--host', 
                        help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('-c', '--config', default='config.yaml',
                        help='Path to YAML config file (default: config.yaml)')
    parser.add_argument('--no-config', action='store_true',
                        help='Ignore config file, use CLI args only')
    parser.add_argument('--init-config', metavar='FILE',
                        help='Generate a default config file and exit')
    parser.add_argument('-u', '--user', action='append', metavar='USER:PASS',
                        help='Add user credentials (can be repeated)')
    parser.add_argument('--upload-dir', 
                        help='Directory for uploads (default: ./uploads)')
    parser.add_argument('--download-dir', 
                        help='Directory for downloads (default: ./downloads)')
    parser.add_argument('--host-key', 
                        help='Path to host key file (default: ./tinyscp_host_key)')
    parser.add_argument('-v', '--version', action='store_true',
                        help='Show version and exit')

    args = parser.parse_args()
    
    # Version
    if args.version:
        from . import __version__
        print(f"tinyscp {__version__}")
        sys.exit(0)
    
    # Setup logging
    setup_logging(args.debug)
    logger = logging.getLogger(__name__)
    
    # Generate config and exit if requested
    if args.init_config:
        save_default_config(args.init_config)
        sys.exit(0)

    # Load config
    if args.no_config:
        config = {
            'host': '0.0.0.0',
            'port': 2222,
            'host_key': './tinyscp_host_key',
            'upload_dir': './uploads',
            'download_dir': './downloads',
            'users': {}
        }
    else:
        config = load_config(args.config)
    
    # CLI args override config file
    if args.port:
        config['port'] = args.port
    if args.host:
        config['host'] = args.host
    if args.upload_dir:
        config['upload_dir'] = args.upload_dir
    if args.download_dir:
        config['download_dir'] = args.download_dir
    if args.host_key:
        config['host_key'] = args.host_key
    
    # Parse CLI users
    if args.user:
        for user_spec in args.user:
            if ':' in user_spec:
                username, password = user_spec.split(':', 1)
                config['users'][username] = password
            else:
                logger.error(f"Invalid user format: {user_spec} (expected USER:PASS)")
                sys.exit(1)
    
    # Create and start server
    server = TinySCPServer(
        host=config['host'],
        port=config['port'],
        host_key_path=config['host_key'],
        upload_dir=config['upload_dir'],
        download_dir=config['download_dir'],
        users=config['users'],
    )
    
    # Handle signals for graceful shutdown
    def signal_handler(signum, frame):
        print()  # newline after ^C
        server.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start server
    try:
        server.start(blocking=True)
    except KeyboardInterrupt:
        server.stop()


if __name__ == '__main__':
    main()
