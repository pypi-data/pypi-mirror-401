#!/usr/bin/env python3
import socket

HOST = "127.0.0.1"
PORT = 9001

# ① 创建 socket（只是创建“端点/把手”，还没建立任何连接）
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.bind((HOST, PORT))
srv.listen(1)
print(f"[server] listening on {HOST}:{PORT}")

# ② accept() 会等待客户端 connect()，连接建立后才返回一个“已连接 socket”
conn, addr = srv.accept()
print(f"[server] accepted from {addr} (TCP channel established)")

data = conn.recv(4096)
print(f"[server] recv: {data!r}")
conn.sendall(b"pong\n")

conn.close()
srv.close()
print("[server] closed")
