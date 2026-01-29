#!/usr/bin/env python3
import socket
import time

HOST = "127.0.0.1"
PORT = 9001

# ① 创建 socket（仍然没连任何人）
cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[client] socket() done (no TCP handshake yet)")

time.sleep(0.5)

# ② connect() 触发 TCP 三次握手，握手成功后才算“通道建立”
cli.connect((HOST, PORT))
print("[client] connect() done (TCP channel established)")

# ③ 有了通道，才能收发字节
cli.sendall(b"ping\n")
resp = cli.recv(4096)
print(f"[client] recv: {resp!r}")

cli.close()
print("[client] closed")
