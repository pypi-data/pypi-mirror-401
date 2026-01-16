"""
TinySCP Server - A minimal bidirectional SCP server

This module provides a lightweight SCP server implementation using Paramiko.
It supports both upload (sink) and download (source) modes.
"""

import os
import sys
import socket
import logging
import threading
from typing import Callable, Optional

import paramiko

logger = logging.getLogger(__name__)


class SCPServer(paramiko.ServerInterface):
    """Paramiko server interface for SCP protocol handling"""
    
    def __init__(self, users: dict):
        self.users = users
        self.event = threading.Event()
        self.command: Optional[str] = None
        self.username: Optional[str] = None

    def check_auth_password(self, username: str, password: str) -> int:
        logger.debug(f"Auth attempt: {username}")
        if username in self.users and self.users[username] == password:
            logger.debug(f"Auth successful for {username}")
            self.username = username
            return paramiko.AUTH_SUCCESSFUL
        logger.debug("Auth failed")
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind: str, chanid: int) -> int:
        logger.debug(f"Channel request: {kind}")
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_exec_request(self, channel, command: bytes) -> bool:
        logger.debug(f"Exec request: {command}")
        self.command = command.decode()
        self.event.set()
        return True


def handle_scp_upload(
    channel,
    command: str,
    upload_dir: str,
    on_upload_complete: Optional[Callable[[str, int, str], None]] = None
) -> None:
    """
    Handle 'scp -t <path>' (sink mode) - client uploading to server
    
    Args:
        channel: Paramiko channel
        command: The SCP command string
        upload_dir: Directory to store uploaded files
        on_upload_complete: Optional callback(filepath, size, username)
    """
    logger.debug(f"Starting upload handler for: {command}")

    # Send ready signal
    channel.send(b'\x00')
    logger.debug("Sent ready signal")

    while True:
        # Read the control line (e.g., "C0644 12345 filename.bin\n")
        line = b''
        while not line.endswith(b'\n'):
            chunk = channel.recv(1024)
            logger.debug(f"Received chunk: {chunk}")
            if not chunk:
                logger.debug("No more data, returning")
                return
            line += chunk

        line = line.decode().strip()
        logger.debug(f"Control line: {line}")

        if not line:
            continue

        if line.startswith('C'):  # File transfer
            parts = line[1:].split(' ', 2)
            mode, size, filename = parts[0], int(parts[1]), parts[2]
            
            # Security: prevent path traversal
            filename = os.path.basename(filename)
            logger.debug(f"File incoming: {filename}, size: {size}, mode: {mode}")

            # Acknowledge
            channel.send(b'\x00')
            logger.debug("Sent file ACK")

            # Receive file data
            filepath = os.path.join(upload_dir, filename)
            received = 0
            with open(filepath, 'wb') as f:
                while received < size:
                    chunk = channel.recv(min(8192, size - received))
                    if not chunk:
                        logger.warning("Connection lost during transfer")
                        break
                    f.write(chunk)
                    received += len(chunk)
                    logger.debug(f"Progress: {received}/{size}")

            # Read trailing null byte
            channel.recv(1)
            # Acknowledge completion
            channel.send(b'\x00')
            logger.info(f"Received: {filename} ({size} bytes)")
            
            # Fire callback if provided
            if on_upload_complete:
                try:
                    on_upload_complete(filepath, size, filename)
                except Exception as e:
                    logger.error(f"Upload callback failed: {e}")

        elif line.startswith('D'):  # Directory (not fully supported)
            logger.debug("Directory mode not supported, sending ACK")
            channel.send(b'\x00')

        elif line.startswith('E') or line == '':
            logger.debug("End of transfer")
            break


def handle_scp_download(
    channel,
    command: str,
    download_dir: str,
    on_download_complete: Optional[Callable[[str, int, str], None]] = None
) -> None:
    """
    Handle 'scp -f <path>' (source mode) - client downloading from server
    
    Args:
        channel: Paramiko channel
        command: The SCP command string
        download_dir: Directory to serve files from
        on_download_complete: Optional callback(filepath, size, username)
    """
    logger.debug(f"Starting download handler for: {command}")
    
    # Parse the requested path from command (e.g., "scp -f /path/to/file")
    parts = command.split()
    if len(parts) < 3:
        logger.debug("Invalid download command")
        channel.send(b'\x01scp: invalid command\n')
        return
    
    requested_path = parts[-1]
    # Security: only allow files from download_dir
    filename = os.path.basename(requested_path)
    filepath = os.path.join(download_dir, filename)
    
    logger.debug(f"Requested file: {filename} -> {filepath}")
    
    if not os.path.exists(filepath):
        error_msg = f"scp: {filename}: No such file\n"
        logger.debug(error_msg.strip())
        channel.send(b'\x01' + error_msg.encode())
        return
    
    if not os.path.isfile(filepath):
        error_msg = f"scp: {filename}: Not a regular file\n"
        logger.debug(error_msg.strip())
        channel.send(b'\x01' + error_msg.encode())
        return
    
    # Get file info
    file_size = os.path.getsize(filepath)
    file_mode = oct(os.stat(filepath).st_mode)[-4:]
    
    # Send file header: C<mode> <size> <filename>\n
    header = f"C{file_mode} {file_size} {filename}\n"
    logger.debug(f"Sending header: {header.strip()}")
    channel.send(header.encode())
    
    # Wait for ACK
    response = channel.recv(1)
    logger.debug(f"Got response: {response}")
    if response != b'\x00':
        logger.debug("Client rejected transfer")
        return
    
    # Send file contents
    logger.debug(f"Sending {file_size} bytes")
    sent = 0
    with open(filepath, 'rb') as f:
        while sent < file_size:
            chunk = f.read(8192)
            if not chunk:
                break
            channel.send(chunk)
            sent += len(chunk)
            logger.debug(f"Progress: {sent}/{file_size}")
    
    # Send completion null byte
    channel.send(b'\x00')
    
    # Wait for final ACK
    response = channel.recv(1)
    logger.debug(f"Final response: {response}")
    
    logger.info(f"Sent: {filename} ({file_size} bytes)")
    
    # Fire callback if provided
    if on_download_complete:
        try:
            on_download_complete(filepath, file_size, filename)
        except Exception as e:
            logger.error(f"Download callback failed: {e}")


class TinySCPServer:
    """
    A minimal bidirectional SCP server.
    
    Example usage:
        server = TinySCPServer(
            users={'admin': 'secret'},
            upload_dir='./uploads',
            download_dir='./downloads'
        )
        server.start()
    """
    
    def __init__(
        self,
        host: str = '0.0.0.0',
        port: int = 2222,
        host_key_path: str = './tinyscp_host_key',
        upload_dir: str = './uploads',
        download_dir: str = './downloads',
        users: Optional[dict] = None,
        on_upload_complete: Optional[Callable[[str, int, str], None]] = None,
        on_download_complete: Optional[Callable[[str, int, str], None]] = None,
    ):
        """
        Initialize the SCP server.
        
        Args:
            host: Host to bind to
            port: Port to listen on
            host_key_path: Path to RSA host key (created if doesn't exist)
            upload_dir: Directory for uploaded files
            download_dir: Directory to serve files from
            users: Dict of username: password pairs
            on_upload_complete: Callback after successful upload
            on_download_complete: Callback after successful download
        """
        self.host = host
        self.port = port
        self.host_key_path = host_key_path
        self.upload_dir = upload_dir
        self.download_dir = download_dir
        self.users = users or {}
        self.on_upload_complete = on_upload_complete
        self.on_download_complete = on_download_complete
        
        self._socket: Optional[socket.socket] = None
        self._host_key: Optional[paramiko.RSAKey] = None
        self._running = False
    
    def _load_or_create_host_key(self) -> paramiko.RSAKey:
        """Load existing host key or generate and save a new one"""
        if os.path.exists(self.host_key_path):
            logger.debug(f"Loading host key from {self.host_key_path}")
            return paramiko.RSAKey.from_private_key_file(self.host_key_path)
        else:
            logger.debug(f"Generating new host key, saving to {self.host_key_path}")
            key = paramiko.RSAKey.generate(2048)
            key.write_private_key_file(self.host_key_path)
            os.chmod(self.host_key_path, 0o600)
            logger.info(f"Generated new host key: {self.host_key_path}")
            return key
    
    def _handle_client(self, client: socket.socket, addr: tuple) -> None:
        """Handle a single client connection"""
        logger.info(f"Connection from {addr}")
        
        try:
            transport = paramiko.Transport(client)
            transport.add_server_key(self._host_key)
            logger.debug("Transport created, starting server")

            server = SCPServer(self.users)
            transport.start_server(server=server)

            channel = transport.accept(20)
            if channel is None:
                logger.debug("No channel established")
                return

            logger.debug("Channel established, waiting for command...")
            server.event.wait(10)

            if server.command:
                logger.debug(f"Command received: {server.command}")
                if '-t' in server.command:
                    # Upload (sink mode)
                    handle_scp_upload(
                        channel, server.command, self.upload_dir,
                        self.on_upload_complete
                    )
                elif '-f' in server.command:
                    # Download (source mode)
                    handle_scp_download(
                        channel, server.command, self.download_dir,
                        self.on_download_complete
                    )
                else:
                    logger.debug(f"Unsupported command mode: {server.command}")
            else:
                logger.debug("No command received (timeout?)")

            channel.close()
            transport.close()

        except Exception as e:
            logger.error(f"Client handler error: {e}", exc_info=True)
    
    def start(self, blocking: bool = True) -> None:
        """
        Start the SCP server.
        
        Args:
            blocking: If True, block until shutdown. If False, run in background thread.
        """
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.download_dir, exist_ok=True)
        
        self._host_key = self._load_or_create_host_key()
        
        if not self.users:
            logger.warning("No users configured! Add users to serve clients.")
        
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self.host, self.port))
        self._socket.listen(5)
        
        self._running = True
        
        logger.info(f"TinySCP Server listening on {self.host}:{self.port}")
        logger.debug(f"Upload directory: {os.path.abspath(self.upload_dir)}")
        logger.debug(f"Download directory: {os.path.abspath(self.download_dir)}")
        logger.debug(f"Configured users: {list(self.users.keys())}")
        
        if blocking:
            self._serve_forever()
        else:
            thread = threading.Thread(target=self._serve_forever, daemon=True)
            thread.start()
    
    def _serve_forever(self) -> None:
        """Main server loop"""
        try:
            while self._running:
                try:
                    self._socket.settimeout(1.0)
                    client, addr = self._socket.accept()
                    thread = threading.Thread(
                        target=self._handle_client,
                        args=(client, addr),
                        daemon=True
                    )
                    thread.start()
                except socket.timeout:
                    continue
        except Exception as e:
            if self._running:
                logger.error(f"Server error: {e}", exc_info=True)
    
    def stop(self) -> None:
        """Stop the SCP server"""
        logger.info("Shutting down...")
        self._running = False
        if self._socket:
            self._socket.close()
