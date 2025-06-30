import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

class PredictiveMaintenanceModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def generate_synthetic_data(self, n_samples=1000):
        """Generate synthetic sensor data for training"""
        np.random.seed(42)
        
        # Generate normal operating conditions
        normal_temp = np.random.normal(70, 10, n_samples//2)  # Normal temperature around 70°C
        normal_vibration = np.random.normal(0.2, 0.05, n_samples//2)  # Low vibration
        normal_pressure = np.random.normal(15, 2, n_samples//2)  # Normal pressure around 15 psi
        
        # Generate failure conditions
        failure_temp = np.random.normal(90, 15, n_samples//2)  # High temperature
        failure_vibration = np.random.normal(0.8, 0.2, n_samples//2)  # High vibration
        failure_pressure = np.random.normal(8, 3, n_samples//2)  # Low pressure (leak)
        
        # Combine data
        temperature = np.concatenate([normal_temp, failure_temp])
        vibration = np.concatenate([normal_vibration, failure_vibration])
        pressure = np.concatenate([normal_pressure, failure_pressure])
        
        # Create labels (0 = normal, 1 = failure risk)
        labels = np.concatenate([np.zeros(n_samples//2), np.ones(n_samples//2)])
        
        # Create DataFrame
        data = pd.DataFrame({
            'temperature': temperature,
            'vibration': vibration,
            'pressure': pressure,
            'failure': labels
        })
        
        return data.sample(frac=1).reset_index(drop=True)  # Shuffle data
    
    def train_model(self):
        """Train the predictive maintenance model"""
        # Generate synthetic training data
        data = self.generate_synthetic_data()
        
        # Prepare features and target
        X = data[['temperature', 'vibration', 'pressure']]
        y = data['failure']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        print(f"Training accuracy: {train_score:.3f}")
        print(f"Testing accuracy: {test_score:.3f}")
        
        self.is_trained = True
        return train_score, test_score
    
    def predict_failure_probability(self, temperature, vibration, pressure):
        """Predict failure probability for given sensor readings"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Prepare input data
        input_data = np.array([[temperature, vibration, pressure]])
        input_scaled = self.scaler.transform(input_data)
        
        # Get prediction probability
        failure_probability = self.model.predict_proba(input_scaled)[0][1]
        
        return failure_probability * 100  # Return as percentage
    
    def get_machine_status(self, failure_probability):
        """Determine machine status based on failure probability"""
        if failure_probability < 30:
            return "Healthy"
        elif failure_probability < 70:
            return "At Risk"
        else:
            return "Failure"
    
    def get_alert_level(self, failure_probability):
        """Get alert level based on failure probability"""
        if failure_probability < 30:
            return "normal"  # Green
        elif failure_probability < 70:
            return "warning"  # Yellow
        else:
            return "critical"  # Red
    
    def save_model(self, filepath):
        """Save the trained model and scaler"""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'is_trained': self.is_trained
        }
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load a pre-trained model and scaler"""
        if os.path.exists(filepath):
            model_data = joblib.load(filepath)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.is_trained = model_data['is_trained']
            print(f"Model loaded from {filepath}")
        else:
            print(f"Model file {filepath} not found. Training new model...")
            self.train_model()
            self.save_model(filepath)

# Initialize and train model if this file is run directly
if __name__ == "__main__":
    model = PredictiveMaintenanceModel()
    model.train_model()
    
    # Test prediction
    temp, vib, press = 85, 0.6, 12
    prob = model.predict_failure_probability(temp, vib, press)
    status = model.get_machine_status(prob)
    alert = model.get_alert_level(prob)
    
    print(f"\nTest prediction:")
    print(f"Sensor readings: Temp={temp}°C, Vibration={vib} m/s², Pressure={press} psi")
    print(f"Failure probability: {prob:.1f}%")
    print(f"Machine status: {status}")
    print(f"Alert level: {alert}")

