# Predictive Failure Monitor - Deployment Guide

## 🚀 Deploy to Render (Recommended)

### Method 1: Using render.yaml (Automatic)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Predictive Failure Monitor"
   git branch -M main
   git remote add origin https://github.com/yourusername/predictive-dashboard.git
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and deploy

### Method 2: Manual Web Service

1. **Create New Web Service** on Render
2. **Connect GitHub Repository**
3. **Configure Settings**:
   - **Build Command**: `cd predictive-backend && pip install -r requirements.txt`
   - **Start Command**: `cd predictive-backend && python src/main.py`
   - **Environment**: Python 3.11
   - **Plan**: Free

## 🌐 Alternative Deployment Options

### Railway
1. Connect GitHub repository
2. Set build command: `cd predictive-backend && pip install -r requirements.txt`
3. Set start command: `cd predictive-backend && python src/main.py`

### Heroku
1. Create `Procfile` in root:
   ```
   web: cd predictive-backend && python src/main.py
   ```
2. Deploy via Heroku CLI or GitHub integration

### DigitalOcean App Platform
1. Create new app from GitHub
2. Configure Python component with above build/start commands

## 🔧 Environment Variables

No environment variables are required for basic deployment. The app works out of the box!

Optional variables:
- `PORT`: Server port (default: 5000)
- `FLASK_ENV`: Set to 'production' for production deployment

## 📝 Post-Deployment

After deployment, your dashboard will be available at your service URL. The ML model will automatically train on first startup (takes ~10 seconds).

## 🐛 Troubleshooting Deployment

### Common Issues:
1. **Build Fails**: Ensure `requirements.txt` is up to date
2. **App Won't Start**: Check that Flask app listens on `0.0.0.0`
3. **Static Files Not Found**: Ensure frontend is built and copied to `src/static/`

### Logs to Check:
- Build logs for dependency installation issues
- Runtime logs for Flask startup and ML model training

