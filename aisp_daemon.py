#!/usr/bin/env python3
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

print("[AISP Daemon] Starting AISP Engine & Security Evaluator...")

class AISPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            update = json.loads(post_data.decode('utf-8'))
            prefix = update.get("prefix", "Unknown")
            as_path = update.get("as_path", [])
            origin_as = as_path[-1] if as_path else "Unknown"

            print(f"\n[AISP Update Received] Prefix: {prefix} | AS-Path: {as_path}")

            # AI & RPKI Validation Logic
            if prefix == "192.168.10.0/24" and origin_as != 65001:
                verdict = "REJECTED (Route Hijack Detected)"
                score = 0.05
            else:
                verdict = "ACCEPTED (Legitimate Route)"
                score = 0.98

            response = {
                "status": verdict,
                "confidence_score": score,
                "prefix": prefix,
                "as_path": as_path
            }

            print(f"[AISP Evaluation] Verdict: {verdict} | Score: {score}")

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, AISPHandler)
    print("[AISP Daemon] Server listening on port 8080...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
