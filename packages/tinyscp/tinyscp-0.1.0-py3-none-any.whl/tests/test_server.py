"""
Basic tests for TinySCP
"""

import os
import time
import tempfile
import pytest

from tinyscp import TinySCPServer, __version__


def test_version():
    """Test version is defined"""
    assert __version__ is not None
    assert isinstance(__version__, str)


def test_server_init():
    """Test server initialization with defaults"""
    server = TinySCPServer(users={'test': 'test'})
    assert server.host == '0.0.0.0'
    assert server.port == 2222
    assert server.users == {'test': 'test'}


def test_server_init_custom():
    """Test server initialization with custom values"""
    server = TinySCPServer(
        host='127.0.0.1',
        port=3333,
        users={'admin': 'secret'},
        upload_dir='/tmp/uploads',
        download_dir='/tmp/downloads'
    )
    assert server.host == '127.0.0.1'
    assert server.port == 3333
    assert server.users == {'admin': 'secret'}
    assert server.upload_dir == '/tmp/uploads'
    assert server.download_dir == '/tmp/downloads'


def test_server_creates_directories():
    """Test that server creates upload/download directories"""
    with tempfile.TemporaryDirectory() as tmpdir:
        upload_dir = os.path.join(tmpdir, 'uploads')
        download_dir = os.path.join(tmpdir, 'downloads')

        server = TinySCPServer(
            port=22221,  # Unique port
            users={'test': 'test'},
            upload_dir=upload_dir,
            download_dir=download_dir,
            host_key_path=os.path.join(tmpdir, 'host_key')
        )

        # Directories are created on start(), not init
        assert not os.path.exists(upload_dir)
        assert not os.path.exists(download_dir)

        # Start in non-blocking mode briefly
        server.start(blocking=False)

        try:
            assert os.path.exists(upload_dir)
            assert os.path.exists(download_dir)
        finally:
            server.stop()
            time.sleep(0.1)  # Brief delay for socket cleanup


def test_host_key_generation():
    """Test that host key is generated if not exists"""
    with tempfile.TemporaryDirectory() as tmpdir:
        key_path = os.path.join(tmpdir, 'test_host_key')

        server = TinySCPServer(
            port=22222,  # Unique port
            users={'test': 'test'},
            host_key_path=key_path,
            upload_dir=os.path.join(tmpdir, 'up'),
            download_dir=os.path.join(tmpdir, 'down')
        )

        assert not os.path.exists(key_path)

        server.start(blocking=False)

        try:
            assert os.path.exists(key_path)
            # Check file permissions (should be 0600)
            mode = os.stat(key_path).st_mode & 0o777
            assert mode == 0o600
        finally:
            server.stop()
            time.sleep(0.1)  # Brief delay for socket cleanup