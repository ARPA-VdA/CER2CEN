import http.server
import logging

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self._handle_request()

    def do_POST(self):
        self._handle_request()

    def _handle_request(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length else b''

        logging.info(f"Received request:\n{self.requestline}\nHeaders:\n{self.headers}\nBody:\n{body.decode('utf-8', errors='replace')}")
        
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server_address = ('', 8082)
    httpd = http.server.HTTPServer(server_address, RequestHandler)
    logging.info("Starting server on port 8082...")
    httpd.serve_forever()