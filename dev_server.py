"""
EcoPulse AI — Unified Local Development Server
Serves static frontend assets from /public and routes API calls to Python serverless handlers.
Run locally with:
    python dev_server.py
Access dashboard at:
    http://localhost:3000
"""

import os
import sys
import json
import mimetypes
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler

# Add root directory to sys.path so api modules can be imported
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)

from api.iot_telemetry import generate_telemetry
from api.ai_audit import run_audit
from api.vfd_analytics import compute_vfd

PORT = 3000
PUBLIC_DIR = os.path.join(ROOT_DIR, "public")


class UnifiedDevHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        # ── API Route 1: IoT Hardware Telemetry ──────────────────────────────
        if path == "/api/iot":
            payload = generate_telemetry()
            body = json.dumps(payload, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return

        # ── API Route 2: AI Anomaly Audit ───────────────────────────────────
        if path == "/api/audit":
            payload = run_audit()
            body = json.dumps(payload, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return

        # ── API Route 3: VFD Calculator ─────────────────────────────────────
        if path == "/api/vfd":
            try:
                speed = float(params.get("speed", ["80"])[0])
            except (ValueError, TypeError, IndexError):
                speed = 80.0
            payload = compute_vfd(speed)
            body = json.dumps(payload, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return

        # ── Static File Route (public directory) ─────────────────────────────
        rel_path = path.lstrip("/")
        if not rel_path or rel_path == "":
            rel_path = "index.html"

        file_path = os.path.join(PUBLIC_DIR, rel_path)
        # Security check: prevent directory traversal
        if not os.path.abspath(file_path).startswith(PUBLIC_DIR):
            self.send_error(403, "Forbidden")
            return

        if os.path.isdir(file_path):
            file_path = os.path.join(file_path, "index.html")

        if os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = "application/octet-stream"

            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, f"File not found: {path}")


def run():
    server = HTTPServer(("0.0.0.0", PORT), UnifiedDevHandler)
    print("=" * 70)
    print(f"⚡ EcoPulse AI // TIET Smart Campus Platform")
    print(f"   Local Full-Stack Server running at http://localhost:{PORT}")
    print(f"   API Endpoints:")
    print(f"     • http://localhost:{PORT}/api/iot")
    print(f"     • http://localhost:{PORT}/api/audit")
    print(f"     • http://localhost:{PORT}/api/vfd?speed=80")
    print("=" * 70)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.server_close()


if __name__ == "__main__":
    run()
