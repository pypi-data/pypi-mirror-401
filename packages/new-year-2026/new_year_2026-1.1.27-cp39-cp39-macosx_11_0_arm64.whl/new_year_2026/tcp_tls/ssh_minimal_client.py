#!/usr/bin/env python3
"""
Minimal SSH handshake demo (banner exchange only).

This is NOT a full SSH implementation. It only shows how to:
1) open a TCP connection to an SSH server
2) read the server's identification string (banner)
3) send the client's identification string
"""

import socket

HOST = "127.0.0.1"
PORT = 22
CLIENT_BANNER = b"SSH-2.0-minimal_client\r\n"

with socket.create_connection((HOST, PORT), timeout=5) as sock:
    # SSH servers send a banner line like: SSH-2.0-OpenSSH_8.9
    banner = sock.recv(256)
    print(f"[client] server banner: {banner!r}")

    # Send our client identification string
    sock.sendall(CLIENT_BANNER)
    print(f"[client] sent banner: {CLIENT_BANNER!r}")
