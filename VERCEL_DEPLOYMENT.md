# Vercel Deployment Guide

This project has been restructured for deployment on Vercel. Here's how to deploy it:

## Project Structure

```
├── api/                    # Serverless API functions
│   ├── predict.py         # ML prediction endpoints
│   ├── users.py           # User management endpoints
│   ├── ml_model.py        # ML model class
│   └── trained_model.pkl  # Pre-trained model
├── src/                   # Frontend source code
│   ├── App.jsx           # Main React component
│   ├── App.css           # Styles
│   ├── main.jsx          # React entry point
│   └── index.html        # HTML template
├── components/            # UI components
│   └── ui/               # Reusable UI components
├── public/               # Static assets
├── dist/                 # Build output (generated)
├── package.json          # Node.js dependencies
├── vite.config.js        # Vite configuration
├── vercel.json           # Vercel deployment config
└── requirements.txt      # Python dependencies

```

## Deployment Steps

### 1. Install Vercel CLI (if not already installed)
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy the project
```bash
vercel --prod
```

## API Endpoints

The following API endpoints are available:

- `GET /api/machine-status` - Get current machine status
- `GET /api/sensor-data` - Get current sensor readings
- `POST /api/predict` - Predict failure probability
- `GET /api/historical-data` - Get historical data
- `GET /api/users` - Get all users
- `POST /api/users` - Create a new user

## Environment Variables

No environment variables are required for basic functionality. The application uses:
- In-memory storage for user data
- Fallback ML model if scikit-learn is not available
- CORS enabled for all origins

## Local Development

### Frontend Development
```bash
npm install
npm run dev
```

### API Testing
```bash
python3 dev-server.py
```

### Build for Production
```bash
npm run build
```

## Features

- ✅ Serverless API functions
- ✅ React frontend with Vite
- ✅ ML-powered failure prediction
- ✅ Real-time sensor data simulation
- ✅ Historical data tracking
- ✅ User management
- ✅ CORS enabled
- ✅ Responsive design
- ✅ No database dependencies

## Notes

- The ML model uses a fallback implementation if scikit-learn is not available
- User data is stored in memory (resets on function restart)
- Historical data is limited to the last 100 readings
- All API endpoints support CORS for frontend integration