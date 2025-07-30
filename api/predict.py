from http.server import BaseHTTPRequestHandler
import json
import random
import time
import os
import sys

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Try to import the ML model from the same directory
    import importlib.util
    spec = importlib.util.spec_from_file_location("ml_model", os.path.join(os.path.dirname(__file__), "ml_model.py"))
    ml_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ml_module)
    PredictiveMaintenanceModel = ml_module.PredictiveMaintenanceModel
    
    # Initialize ML model with local model file
    model = PredictiveMaintenanceModel()
    model_path = os.path.join(os.path.dirname(__file__), 'trained_model.pkl')
    try:
        model.load_model(model_path)
    except:
        model.train_model()
        
except ImportError:
    # Fallback for when ml_model is not available
    class PredictiveMaintenanceModel:
        def __init__(self):
            self.is_trained = True
        
        def predict_failure_probability(self, temp, vib, press):
            # Simple fallback prediction based on thresholds
            score = 0
            if temp > 80: score += 30
            elif temp > 70: score += 15
            if vib > 0.5: score += 25
            elif vib > 0.3: score += 10
            if press < 10: score += 25
            elif press < 13: score += 10
            return min(score + random.uniform(0, 20), 100)
        
        def get_machine_status(self, prob):
            if prob < 30: return "Healthy"
            elif prob < 70: return "At Risk"
            else: return "Failure"
        
        def get_alert_level(self, prob):
            if prob < 30: return "normal"
            elif prob < 70: return "warning"
            else: return "critical"
    
    # Initialize fallback model
    model = PredictiveMaintenanceModel()

# Store historical data (in production, this would be a database)
historical_data = []

def generate_realistic_sensor_data():
    """Generate realistic sensor data with some variation"""
    condition = random.choice(['normal', 'warning', 'critical'])
    
    if condition == 'normal':
        temperature = random.uniform(65, 75)
        vibration = random.uniform(0.1, 0.3)
        pressure = random.uniform(13, 17)
    elif condition == 'warning':
        temperature = random.uniform(75, 85)
        vibration = random.uniform(0.3, 0.6)
        pressure = random.uniform(10, 13)
    else:  # critical
        temperature = random.uniform(85, 95)
        vibration = random.uniform(0.6, 1.0)
        pressure = random.uniform(5, 10)
    
    return {
        'temperature': round(temperature, 1),
        'vibration': round(vibration, 2),
        'pressure': round(pressure, 1),
        'timestamp': time.time()
    }

def handle_sensor_data():
    """Get current sensor readings"""
    try:
        sensor_data = generate_realistic_sensor_data()
        
        # Get ML prediction
        failure_prob = model.predict_failure_probability(
            sensor_data['temperature'],
            sensor_data['vibration'],
            sensor_data['pressure']
        )
        
        machine_status = model.get_machine_status(failure_prob)
        alert_level = model.get_alert_level(failure_prob)
        
        # Store in historical data (keep last 100 readings)
        data_point = {
            **sensor_data,
            'failure_probability': round(failure_prob, 1),
            'machine_status': machine_status,
            'alert_level': alert_level
        }
        
        historical_data.append(data_point)
        if len(historical_data) > 100:
            historical_data.pop(0)
        
        return {
            'success': True,
            'data': data_point
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def handle_predict(body):
    """Predict failure probability for given sensor data"""
    try:
        data = json.loads(body) if body else {}
        
        if not data or not all(key in data for key in ['temperature', 'vibration', 'pressure']):
            return {
                'success': False,
                'error': 'Missing required sensor data: temperature, vibration, pressure'
            }, 400
        
        temperature = float(data['temperature'])
        vibration = float(data['vibration'])
        pressure = float(data['pressure'])
        
        # Get prediction
        failure_prob = model.predict_failure_probability(temperature, vibration, pressure)
        machine_status = model.get_machine_status(failure_prob)
        alert_level = model.get_alert_level(failure_prob)
        
        return {
            'success': True,
            'data': {
                'temperature': temperature,
                'vibration': vibration,
                'pressure': pressure,
                'failure_probability': round(failure_prob, 1),
                'machine_status': machine_status,
                'alert_level': alert_level,
                'timestamp': time.time()
            }
        }
    
    except ValueError as e:
        return {
            'success': False,
            'error': f'Invalid input data: {str(e)}'
        }, 400
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }, 500

def handle_historical_data(query_params):
    """Get historical sensor data and predictions"""
    try:
        # Get last N data points
        limit = int(query_params.get('limit', [50])[0])
        limit = min(limit, len(historical_data))  # Don't exceed available data
        
        recent_data = historical_data[-limit:] if historical_data else []
        
        return {
            'success': True,
            'data': recent_data,
            'count': len(recent_data)
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def handle_machine_status():
    """Get current machine status summary"""
    try:
        if not historical_data:
            # Generate initial data if none exists
            sensor_data = generate_realistic_sensor_data()
            failure_prob = model.predict_failure_probability(
                sensor_data['temperature'],
                sensor_data['vibration'],
                sensor_data['pressure']
            )
            machine_status = model.get_machine_status(failure_prob)
            alert_level = model.get_alert_level(failure_prob)
            
            current_data = {
                **sensor_data,
                'failure_probability': round(failure_prob, 1),
                'machine_status': machine_status,
                'alert_level': alert_level
            }
        else:
            current_data = historical_data[-1]
        
        return {
            'success': True,
            'data': {
                'machine_id': 'MACHINE-001',
                'machine_name': 'Production Line A',
                'current_status': current_data['machine_status'],
                'alert_level': current_data['alert_level'],
                'failure_probability': current_data['failure_probability'],
                'last_updated': current_data['timestamp'],
                'sensor_readings': {
                    'temperature': current_data['temperature'],
                    'vibration': current_data['vibration'],
                    'pressure': current_data['pressure']
                }
            }
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?')[0]
        query_params = {}
        
        if '?' in self.path:
            query_string = self.path.split('?')[1]
            for param in query_string.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    if key in query_params:
                        if not isinstance(query_params[key], list):
                            query_params[key] = [query_params[key]]
                        query_params[key].append(value)
                    else:
                        query_params[key] = [value]
        
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if path == '/api/sensor-data':
            result = handle_sensor_data()
        elif path == '/api/historical-data':
            result = handle_historical_data(query_params)
        elif path == '/api/machine-status':
            result = handle_machine_status()
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
        
        if self.path == '/api/predict':
            result = handle_predict(body)
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