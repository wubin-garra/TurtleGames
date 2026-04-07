#!/usr/bin/env python3
"""Simple HTTP server with CORS proxy for Polymarket API."""
import http.server
import urllib.request
import json
import os

PORT = 8000
DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def do_GET(self):
        # Proxy requests to /api/* -> gamma-api.polymarket.com/*
        if self.path.startswith('/api/'):
            self.proxy_polymarket()
        else:
            super().do_GET()

    def proxy_polymarket(self):
        target = 'https://gamma-api.polymarket.com' + self.path[4:]  # strip /api
        try:
            req = urllib.request.Request(target, headers={'User-Agent': 'PredictionGlobe/1.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
        except Exception as e:
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

print(f'Serving on http://localhost:{PORT}')
http.server.HTTPServer(('', PORT), Handler).serve_forever()
