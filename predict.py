from flask import Blueprint, request, jsonify
import random
import time
import os
from src.models.ml_model import PredictiveMaintenanceModel

# Create blueprint
predict_bp = Blueprint('predict', __name__)

# Initialize ML model
model = PredictiveMaintenanceModel()
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'trained_model.pkl')

# Load or train model
try:
    model.load_model(model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    print("Training new model...")
    model.train_model()
    model.save_model(model_path)

# Store historical data (in production, this would be a database)
historical_data = []

def generate_realistic_sensor_data():
    """Generate realistic sensor data with some variation"""
    base_time = time.time()
    
    # Simulate different machine conditions
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
        'timestamp': base_time
    }

@predict_bp.route('/sensor-data', methods=['GET'])
def get_sensor_data():
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
        
        return jsonify({
            'success': True,
            'data': data_point
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@predict_bp.route('/predict', methods=['POST'])
def predict_failure():
    """Predict failure probability for given sensor data"""
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['temperature', 'vibration', 'pressure']):
            return jsonify({
                'success': False,
                'error': 'Missing required sensor data: temperature, vibration, pressure'
            }), 400
        
        temperature = float(data['temperature'])
        vibration = float(data['vibration'])
        pressure = float(data['pressure'])
        
        # Get prediction
        failure_prob = model.predict_failure_probability(temperature, vibration, pressure)
        machine_status = model.get_machine_status(failure_prob)
        alert_level = model.get_alert_level(failure_prob)
        
        return jsonify({
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
        })
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid input data: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@predict_bp.route('/historical-data', methods=['GET'])
def get_historical_data():
    """Get historical sensor data and predictions"""
    try:
        # Get last N data points
        limit = request.args.get('limit', 50, type=int)
        limit = min(limit, len(historical_data))  # Don't exceed available data
        
        recent_data = historical_data[-limit:] if historical_data else []
        
        return jsonify({
            'success': True,
            'data': recent_data,
            'count': len(recent_data)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@predict_bp.route('/machine-status', methods=['GET'])
def get_machine_status():
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
        
        return jsonify({
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
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

