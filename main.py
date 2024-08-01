from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import socket
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        try:
            with open(f"front-init{self.path}", "rb") as file:
                self.send_response(200)
                if self.path.endswith(".html"):
                    self.send_header("Content-type", "text/html")
                elif self.path.endswith(".css"):
                    self.send_header("Content-type", "text/css")
                elif self.path.endswith(".png"):
                    self.send_header("Content-type", "image/png")
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, "File Not Found")
            self.path = "/error.html"
            with open(f"front-init{self.path}", "rb") as file:
                self.wfile.write(file.read())

    def do_POST(self):
        if self.path == "/message":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            message_data = {
                'username': post_data['username'][0],
                'message': post_data['message'][0]
            }

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(('localhost', 5000))
                    s.sendall(json.dumps(message_data).encode('utf-8'))
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Message received")
            except ConnectionRefusedError:
                self.send_error(500, "Failed to connect to the socket server")

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 3000)
    httpd = server_class(server_address, handler_class)
    print("Serving HTTP on port 3000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
