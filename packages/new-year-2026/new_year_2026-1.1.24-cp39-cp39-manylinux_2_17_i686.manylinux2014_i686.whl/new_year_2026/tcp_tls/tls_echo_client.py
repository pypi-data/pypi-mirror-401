#!/usr/bin/env python3
"""
最小可跑的 TLS echo client,演示:
- 先建立 TCP,再在其上做 TLS 握手
- 用 cert.pem 当作“受信任的根”（自签时常见做法）
"""
import socket
import ssl

HOST = "127.0.0.1"
PORT = 9443


def main():
    # 1) 客户端信任的 CA/证书，这里直接信任本地自签的 cert.pem
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.check_hostname = False  # 自签证书常常与 hostname 不符，这里关闭 Hostname 校验
    ctx.load_verify_locations("cert.pem")

    # 2) 先做 TCP 连接
    #TODO 加一段详细解析
    with socket.create_connection((HOST, PORT)) as sock:
        print(f"[cli] TCP connected to {HOST}:{PORT}, starting TLS handshake ...")

        # 3) 在 TCP 之上做 TLS，握手成功才算“安全通道”建立
        with ctx.wrap_socket(sock, server_hostname=HOST) as tls_sock:
            print(f"[cli] TLS established: version={tls_sock.version()}, cipher={tls_sock.cipher()}")
            print(f"[cli] server cert subject={tls_sock.getpeercert().get('subject')}")

            tls_sock.sendall(b"hi TLS server\n")
            resp = tls_sock.recv(4096)
            print(f"[cli] recv (decrypted): {resp!r}")

    print("[cli] closed")


if __name__ == "__main__":
    main()
