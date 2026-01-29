#!/usr/bin/env python3
import http.server
import ssl

HOST = "127.0.0.1"
PORT = 8443

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"Hello over HTTPS (HTTP + TLS)!\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # 少打点日志，方便观察
        pass

httpd = http.server.HTTPServer((HOST, PORT), Handler)

# 关键：给 socket 套上 TLS（这一步就是 HTTPS 的核心）
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

print(f"HTTPS server listening on https://{HOST}:{PORT}")
httpd.serve_forever()
