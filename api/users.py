from http.server import BaseHTTPRequestHandler
import json
import os

# Simple in-memory user storage (in production, use a proper database)
users_data = [
    {"id": 1, "username": "admin", "email": "admin@example.com"},
    {"id": 2, "username": "operator", "email": "operator@example.com"}
]

def handle_get_users():
    """Get all users"""
    try:
        return {
            'success': True,
            'data': users_data
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def handle_create_user(body):
    """Create a new user"""
    try:
        data = json.loads(body) if body else {}
        
        if not data or not all(key in data for key in ['username', 'email']):
            return {
                'success': False,
                'error': 'Missing required fields: username, email'
            }, 400
        
        # Check if user already exists
        existing_user = next((u for u in users_data if u['username'] == data['username']), None)
        if existing_user:
            return {
                'success': False,
                'error': 'Username already exists'
            }, 400
        
        existing_email = next((u for u in users_data if u['email'] == data['email']), None)
        if existing_email:
            return {
                'success': False,
                'error': 'Email already exists'
            }, 400
        
        # Create new user
        new_id = max([u['id'] for u in users_data]) + 1 if users_data else 1
        new_user = {
            'id': new_id,
            'username': data['username'],
            'email': data['email']
        }
        users_data.append(new_user)
        
        return {
            'success': True,
            'data': new_user
        }, 201
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }, 500

def handle_get_user(user_id):
    """Get a specific user"""
    try:
        user = next((u for u in users_data if u['id'] == int(user_id)), None)
        if not user:
            return {
                'success': False,
                'error': 'User not found'
            }, 404
        
        return {
            'success': True,
            'data': user
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }, 404

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        path_parts = self.path.split('/')
        
        if self.path == '/api/users':
            result = handle_get_users()
        elif len(path_parts) >= 4 and path_parts[2] == 'users':
            # Handle /api/users/{id}
            user_id = path_parts[3]
            result = handle_get_user(user_id)
        else:
            result = {'success': False, 'error': 'Endpoint not found'}
        
        self.wfile.write(json.dumps(result).encode())
    
    def do_POST(self):
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        
        if self.path == '/api/users':
            result = handle_create_user(body)
        else:
            result = {'success': False, 'error': 'Endpoint not found'}
        
        self.wfile.write(json.dumps(result).encode())
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()