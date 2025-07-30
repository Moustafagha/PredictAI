#!/usr/bin/env python3
"""
Simple development server for testing Vercel API functions locally
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our API handlers
from api.predict import handler as predict_handler
from api.users import handler as users_handler

class DevHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/users'):
            users_handler.do_GET(self)
        elif self.path.startswith('/api/'):
            predict_handler.do_GET(self)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')
    
    def do_POST(self):
        if self.path.startswith('/api/users'):
            users_handler.do_POST(self)
        elif self.path.startswith('/api/'):
            predict_handler.do_POST(self)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')
    
    def do_OPTIONS(self):
        if self.path.startswith('/api/users'):
            users_handler.do_OPTIONS(self)
        elif self.path.startswith('/api/'):
            predict_handler.do_OPTIONS(self)
        else:
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 3000), DevHandler)
    print("Development server running on http://localhost:3000")
    print("API endpoints available at http://localhost:3000/api/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()