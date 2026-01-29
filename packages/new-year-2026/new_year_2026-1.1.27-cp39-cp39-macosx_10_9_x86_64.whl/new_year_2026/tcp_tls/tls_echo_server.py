#!/usr/bin/env python3
"""
最小可跑的 TLS echo server，突出“先有 TCP，再在其上做 TLS 握手”。
需要现成的 cert.pem/key.pem（自签也可以），端口默认 9443。
"""
import socket
import ssl

HOST = "127.0.0.1"
PORT = 9443


def main():
    # 1) 先搭好普通 TCP 监听 socket（还没 TLS）
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((HOST, PORT))
    listener.listen(1)
    print(f"[srv] TCP listening on {HOST}:{PORT}")

    # 2) 准备 TLS 配置（证书链 + 密钥），并要求 TLS1.2+
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    try:
        # 3) 纯 TCP 连接先建立，再触发 TLS 握手
        raw_conn, addr = listener.accept()
        print(f"[srv] TCP connected from {addr}, starting TLS handshake ...")

        with ctx.wrap_socket(raw_conn, server_side=True) as tls_conn:
            print(f"[srv] TLS established: version={tls_conn.version()}, cipher={tls_conn.cipher()}")

            data = tls_conn.recv(4096)
            print(f"[srv] recv (decrypted): {data!r}")
            tls_conn.sendall(b"hello over TLS\n")
            print("[srv] response sent (will be TLS-encrypted on the wire)")
    finally:
        listener.close()
        print("[srv] listener closed")


if __name__ == "__main__":
    main()
