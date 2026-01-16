"""
TinySCP - A minimal bidirectional SCP server

A lightweight, embeddable SCP server for network automation workflows.
Supports both upload (devices pushing images) and download (devices pulling configs).

Example:
    from tinyscp import TinySCPServer
    
    server = TinySCPServer(
        port=2222,
        users={'admin': 'secret'},
        upload_dir='./uploads',
        download_dir='./downloads'
    )
    server.start()

CLI usage:
    tinyscp -c config.yaml
    tinyscp -d -p 2222 -u admin:secret
"""

__version__ = "0.1.0"
__author__ = "Scott Peterman"
__license__ = "MIT"

from .server import TinySCPServer, SCPServer

__all__ = ['TinySCPServer', 'SCPServer', '__version__']
