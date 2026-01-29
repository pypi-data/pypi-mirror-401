#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

class Handler(BaseHTTPRequestHandler):
    def _send_json(self, obj, status=200):
        data = json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        # GET：参数通常在 URL 的 query string 里
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query, keep_blank_values=True)

        self._send_json({
            "method": "GET",
            "path": parsed.path,
            "raw_query": parsed.query,
            "query_params": qs,
            "note": "GET 的参数在 URL 里（?a=1&b=2），一般用于读取/查询"
        })

    def do_POST(self):
        # POST：参数/数据通常在请求体 body 里
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        body_bytes = self.rfile.read(length) if length > 0 else b""
        body_text = body_bytes.decode("utf-8", errors="replace")

        self._send_json({
            "method": "POST",
            "path": parsed.path,
            "content_type": self.headers.get("Content-Type", ""),
            "content_length": length,
            "raw_body": body_text,
            "note": "POST 的数据在 body 里，常用于提交/处理（可能产生副作用）"
        })

def main():
    host = "127.0.0.1"
    port = 8000
    server = HTTPServer((host, port), Handler)
    print(f"Listening on http://{host}:{port}")
    print("Try: curl 'http://127.0.0.1:8000/echo?a=1&b=2'")
    print("Try: curl -X POST 'http://127.0.0.1:8000/echo' -d 'a=1&b=2'")
    server.serve_forever()

if __name__ == "__main__":
    main()
