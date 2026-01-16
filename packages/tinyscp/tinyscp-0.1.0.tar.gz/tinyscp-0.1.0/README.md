# TinySCP

A minimal, embeddable SCP server for network automation workflows.

[![PyPI version](https://badge.fury.io/py/tinyscp.svg)](https://badge.fury.io/py/tinyscp)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why TinySCP?

There are plenty of SCP *clients* for Python, but no lightweight SCP *server*. TinySCP fills that gap—a simple, drop-in SCP server you can embed in your automation workflows or run standalone for:

- **Firmware staging** — Network devices push/pull images
- **Config distribution** — Centralized config server for network gear
- **File collection** — Devices upload logs, captures, or backups
- **Lab environments** — Quick file server without spinning up full SSH infrastructure

## Installation

```bash
pip install tinyscp
```

For YAML config file support:
```bash
pip install tinyscp[yaml]
```

## Quick Start

### CLI Usage

```bash
# Generate a config file
tinyscp --init-config config.yaml

# Edit config.yaml to set your users, then run:
tinyscp

# Or run without config file:
tinyscp --no-config -u admin:secret -p 2222
```

### Development Mode

If running from source without installing:

```bash
# Clone and setup
git clone https://github.com/scottpeterman/tinyscp.git
cd tinyscp
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
pip install -e ".[yaml]"

# Run via module
python -m tinyscp.cli --help
python -m tinyscp.cli --init-config config.yaml
python -m tinyscp.cli -d
```

### Client Usage

Modern macOS/Linux defaults to SFTP mode for `scp`. Use `-O` to force legacy SCP protocol:

```bash
# Upload to server
scp -O -P 2222 firmware.bin admin@server:/uploads/

# Download from server
scp -O -P 2222 admin@server:/downloads/startup-config.txt ./
```

### Python API

```python
from tinyscp import TinySCPServer

# Basic usage
server = TinySCPServer(
    port=2222,
    users={'admin': 'secret'},
    upload_dir='./uploads',
    download_dir='./downloads'
)
server.start()

# With callbacks for post-transfer actions
def on_upload(filepath, size, filename):
    print(f"Received {filename}, verifying checksum...")
    # Validate firmware, trigger deployment, etc.

server = TinySCPServer(
    port=2222,
    users={'admin': 'secret'},
    on_upload_complete=on_upload
)
server.start()

# Non-blocking mode
server.start(blocking=False)
# ... do other things ...
server.stop()
```

## Configuration

### Config File (YAML)

```yaml
host: 0.0.0.0
port: 2222
host_key: ./tinyscp_host_key
upload_dir: ./uploads
download_dir: ./downloads
users:
  admin: changeme
  neteng: firmware123
  backup_svc: b4ckup!
```

### CLI Options

```
usage: tinyscp [-h] [-d] [-p PORT] [-H HOST] [-c CONFIG] [--no-config]
               [--init-config FILE] [-u USER:PASS] [--upload-dir DIR]
               [--download-dir DIR] [--host-key FILE] [-v]

Options:
  -d, --debug           Enable debug output
  -p, --port PORT       Port to listen on (default: 2222)
  -H, --host HOST       Host to bind to (default: 0.0.0.0)
  -c, --config FILE     Path to YAML config file (default: config.yaml)
  --no-config           Ignore config file, use CLI args only
  --init-config FILE    Generate a default config file and exit
  -u, --user USER:PASS  Add user credentials (can be repeated)
  --upload-dir DIR      Directory for uploads (default: ./uploads)
  --download-dir DIR    Directory for downloads (default: ./downloads)
  --host-key FILE       Path to host key file
  -v, --version         Show version and exit
```

## Features

- **Bidirectional transfers** — Both upload (sink) and download (source) modes
- **Persistent host keys** — No more "host key changed" warnings on restart
- **YAML configuration** — Simple config file for users and settings
- **Callback hooks** — Trigger actions on upload/download completion
- **Path traversal protection** — Filenames are sanitized
- **Concurrent connections** — Threaded client handling
- **Embeddable** — Use as a library in your own applications
- **No dependencies** — Just Paramiko (PyYAML optional for config files)

## Security Considerations

TinySCP is designed for trusted network environments (labs, internal infrastructure, automation pipelines). It is **not** intended as a public-facing service.

- Passwords are stored in plain text in config files
- No rate limiting or brute-force protection
- No chroot/jail for uploaded files (though path traversal is blocked)

For production use, consider:
- Running behind a firewall
- Using SSH key authentication (PR welcome!)
- Restricting to specific source IPs

## Contributing

Contributions welcome! Areas of interest:

- SSH key authentication
- SFTP subsystem support
- Transfer progress callbacks
- Recursive directory transfers
- Upload size limits / quotas

## License

MIT License - See [LICENSE](LICENSE) for details.

## Author

Scott Peterman ([@scottpeterman](https://github.com/scottpeterman))

Part of the network automation toolkit alongside:
- [Secure Cartography](https://github.com/scottpeterman/secure_cartography) — Network discovery and mapping
- [UglyPTY](https://github.com/scottpeterman/UglyPTY) — SSH terminal with session management