# Predictive Failure Monitor Dashboard

A complete AI-powered dashboard that predicts machine failures based on real-time sensor data using machine learning.

## 🔥 Features

- **Real-time Machine Status**: Healthy / At Risk / Failure indicators
- **Live Sensor Readings**: Temperature, Vibration, Pressure monitoring
- **AI-Powered Predictions**: Failure probability (0-100%) using Random Forest ML model
- **Smart Alert System**: Green (Normal), Yellow (Warning), Red (Critical)
- **Historical Trends**: Interactive line charts showing sensor data over time
- **Auto-refresh**: Dashboard updates every 5 seconds
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🏗️ Architecture

### Backend (Flask + ML)
- **Framework**: Flask with CORS enabled
- **ML Model**: Random Forest Classifier with synthetic training data
- **API Endpoints**:
  - `/api/machine-status` - Current machine status and sensor readings
  - `/api/sensor-data` - Real-time sensor data with predictions
  - `/api/predict` - Manual prediction endpoint
  - `/api/historical-data` - Historical sensor data for charts

### Frontend (React)
- **Framework**: React with Vite
- **UI Components**: shadcn/ui with Tailwind CSS
- **Charts**: Recharts for historical data visualization
- **Icons**: Lucide React icons
- **Auto-refresh**: Updates every 5 seconds

## 📦 Project Structure

```
predictive-dashboard/
├── predictive-backend/          # Flask backend with ML model
│   ├── src/
│   │   ├── models/
│   │   │   ├── ml_model.py     # ML model implementation
│   │   │   └── trained_model.pkl # Trained model file
│   │   ├── routes/
│   │   │   └── predict.py      # API endpoints
│   │   ├── static/             # Built frontend files
│   │   └── main.py             # Flask app entry point
│   ├── venv/                   # Python virtual environment
│   └── requirements.txt        # Python dependencies
├── predictive-frontend/         # React frontend
│   ├── src/
│   │   ├── components/         # UI components
│   │   ├── App.jsx            # Main dashboard component
│   │   └── App.css            # Styles
│   ├── dist/                  # Built files
│   └── package.json           # Node dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### Local Development

1. **Backend Setup**:
   ```bash
   cd predictive-backend
   source venv/bin/activate
   pip install -r requirements.txt
   python src/main.py
   ```
   Backend will run on `http://localhost:5000`

2. **Frontend Development** (optional, for development):
   ```bash
   cd predictive-frontend
   pnpm install
   pnpm run dev
   ```
   Frontend dev server will run on `http://localhost:5173`

3. **Full-Stack (Recommended)**:
   Just run the backend - it serves the frontend from `/src/static/`

### 🌐 Deployment Options

#### Option 1: Deploy Backend Only (Recommended)
The backend serves the built frontend, so you only need to deploy one service:

1. **Render/Railway/Heroku**:
   - Connect to your GitHub repository
   - Set build command: `cd predictive-backend && pip install -r requirements.txt`
   - Set start command: `cd predictive-backend && python src/main.py`
   - Set port: `5000`

#### Option 2: Separate Frontend/Backend
1. **Backend**: Deploy Flask app as above
2. **Frontend**: Deploy React app to Vercel/Netlify
   - Build command: `cd predictive-frontend && pnpm run build`
   - Publish directory: `predictive-frontend/dist`
   - Set environment variable: `REACT_APP_API_URL=your-backend-url`

## 🧠 ML Model Details

- **Algorithm**: Random Forest Classifier
- **Features**: Temperature, Vibration, Pressure
- **Training Data**: 1000 synthetic samples (500 normal, 500 failure conditions)
- **Accuracy**: ~99.5% on test data
- **Output**: Failure probability (0-100%)

### Status Thresholds:
- **Healthy**: < 30% failure probability (Green)
- **At Risk**: 30-70% failure probability (Yellow)  
- **Failure**: > 70% failure probability (Red)

## 🔧 API Documentation

### GET /api/machine-status
Returns current machine status and sensor readings.

**Response**:
```json
{
  "success": true,
  "data": {
    "machine_id": "MACHINE-001",
    "machine_name": "Production Line A",
    "current_status": "Healthy",
    "alert_level": "normal",
    "failure_probability": 15.2,
    "sensor_readings": {
      "temperature": 72.5,
      "vibration": 0.18,
      "pressure": 14.8
    }
  }
}
```

### GET /api/historical-data?limit=50
Returns historical sensor data and predictions.

### POST /api/predict
Manual prediction endpoint.

**Request**:
```json
{
  "temperature": 85.0,
  "vibration": 0.6,
  "pressure": 12.0
}
```

## 🛠️ Customization

### Adding New Sensors
1. Update `ml_model.py` to include new features
2. Retrain the model with new data
3. Update API endpoints in `predict.py`
4. Add new sensor cards in React frontend

### Changing Alert Thresholds
Modify the thresholds in `ml_model.py`:
```python
def get_machine_status(self, failure_probability):
    if failure_probability < 30:  # Change this
        return "Healthy"
    elif failure_probability < 70:  # And this
        return "At Risk"
    else:
        return "Failure"
```

## 📊 Sample Data

The ML model generates realistic synthetic data:
- **Normal Operation**: Temp ~70°C, Vibration ~0.2 m/s², Pressure ~15 psi
- **Failure Conditions**: Temp ~90°C, Vibration ~0.8 m/s², Pressure ~8 psi

## 🐛 Troubleshooting

### Common Issues:
1. **CORS Errors**: Ensure Flask-CORS is installed and configured
2. **Model Not Found**: The model trains automatically on first run
3. **Port Conflicts**: Change port in `main.py` if 5000 is occupied
4. **Build Errors**: Ensure all dependencies are installed

### Development Tips:
- Use browser dev tools to monitor API calls
- Check Flask console for ML model training logs
- Frontend auto-refreshes every 5 seconds - watch network tab

## 📝 License

MIT License - feel free to use this project as a starting point for your own predictive maintenance solutions!

## 🚀 Next Steps

- Connect to real sensor hardware (IoT devices, PLCs)
- Add user authentication and multi-machine support
- Implement email/SMS alerts for critical conditions
- Add more sophisticated ML models (LSTM for time series)
- Create mobile app version
- Add data export functionality

