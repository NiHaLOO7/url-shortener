from http.server import HTTPServer, BaseHTTPRequestHandler
from src.url_shortener import URLShortener
import json
import time

shortener = URLShortener()

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/shorten":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            url = body.get("url")

            if not url:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "url is required"}).encode())
                return

            short_code = shortener.shorten(url)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"short_code": short_code, "short_url": f"http://localhost:8080/{short_code}"}).encode())

    def do_GET(self):
        short_code = self.path.lstrip("/")

        if not short_code:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "short_code is required"}).encode())
            return

        long_url = shortener.redirect(short_code)

        if not long_url:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "URL not found"}).encode())
            return

        self.send_response(302)
        self.send_header("Location", long_url)
        self.end_headers()

    def log_message(self, _format, *args):
        print(f"[{time.strftime('%H:%M:%S')}] {args[0]} → {args[1]}")

print("Server running on http://localhost:8080")
print('Shorten: curl -X POST http://localhost:8080/shorten -H "Content-Type: application/json" -d \'{"url": "https://youtube.com"}\'')
print("Redirect: open http://localhost:8080/<short_code> in browser\n")
HTTPServer(("", 8080), Handler).serve_forever()
