# GuardAI Deployment Guide

## 🚀 Deploying to Render (Recommended)

Render provides free hosting for web applications and automatically detects our `render.yaml` configuration.

### Prerequisites
- GitHub account with the GuardAI repository
- Render account (free tier available)

### Step-by-Step Deployment

#### 1. Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

#### 2. Create New Web Service
1. Click **"New +"** in the top right
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - Search for your repository name
   - Click **"Connect"**

#### 3. Configure Service
Render will automatically detect `render.yaml` and configure:
- **Name:** guardai-malware-detection
- **Environment:** Docker
- **Build Command:** Auto-detected from Dockerfile
- **Start Command:** `gunicorn -b 0.0.0.0:$PORT src.app:app`

**Important:** Make sure to set environment variables if needed:
- No environment variables required for basic deployment

#### 4. Deploy
1. Click **"Create Web Service"**
2. Render will:
   - Build the Docker image
   - Install dependencies
   - Start the application
3. Wait 5-10 minutes for initial deployment

#### 5. Verify Deployment
Once deployed, you'll get a URL like: `https://guardai-malware-detection.onrender.com`

Test the deployment:
```bash
# Health check
curl https://your-app-url.onrender.com/health

# Expected response:
# {"status": "healthy", "model_loaded": true}
```

#### 6. Access the Dashboard
Open your browser to: `https://your-app-url.onrender.com`

You should see the GuardAI dashboard with:
- ✅ Premium UI with glassmorphism effects
- ✅ Integrated heuristic console
- ✅ Manual prediction and batch upload features

---

## 🔄 Alternative: Railway Deployment

### Quick Deploy to Railway

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **New Project**
   - Click **"New Project"**
   - Select **"Deploy from GitHub repo"**
   - Choose your GuardAI repository

3. **Configure**
   - Railway auto-detects Dockerfile
   - No additional configuration needed

4. **Deploy**
   - Click **"Deploy"**
   - Wait 5-10 minutes
   - Get deployment URL

---

## 🐳 Alternative: Fly.io Deployment

### Deploy with Fly.io

1. **Install Fly CLI**
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Login**
```bash
fly auth login
```

3. **Launch App**
```bash
cd /path/to/new-assignemnt
fly launch
```

4. **Deploy**
```bash
fly deploy
```

5. **Open App**
```bash
fly open
```

---

## ⚠️ Important Notes

### Model Files
The model files (`model.pkl`, `model_metadata.pkl`) are **NOT** included in the repository due to `.gitignore`.

**Solution:** The application will automatically train the model on first startup if files are missing. This adds ~30 seconds to the initial deployment time.

**Alternative:** If you want faster deployment:
1. Remove `*.pkl` from `.gitignore`
2. Commit model files
3. Push to repository
4. Redeploy

### Dataset
The `brazilian-malware.csv` dataset is also gitignored. The application expects it to be present for training.

**For deployment:**
- Include `brazilian-malware.zip` in the repository
- The `setup.sh` script will extract it automatically
- Or modify Dockerfile to download dataset during build

### Environment Variables
No environment variables are required for basic deployment. The application uses default configurations.

---

## 🧪 Post-Deployment Testing

### 1. Health Check
```bash
curl https://your-app-url.onrender.com/health
```

Expected: `{"status": "healthy", "model_loaded": true}`

### 2. Manual Prediction Test
1. Open dashboard in browser
2. Click "Seed Malware"
3. Click "Analyze Threat"
4. Verify result shows "CRITICAL THREAT"

### 3. Batch Upload Test
1. Upload `sample_test.csv`
2. Verify batch results display
3. Test "Export Forensic Report" button

---

## 📊 Monitoring

### Render Dashboard
- View logs: Click on your service → "Logs" tab
- Monitor metrics: "Metrics" tab shows CPU, memory usage
- Restart service: "Manual Deploy" → "Clear build cache & deploy"

### Common Issues

**Issue:** Model not loading
- **Solution:** Check logs for training output, ensure dataset is available

**Issue:** Slow initial load
- **Solution:** Normal - model training takes ~30 seconds on first startup

**Issue:** 503 Service Unavailable
- **Solution:** Wait for deployment to complete, check logs for errors

---

## 🔗 Submission Checklist

After successful deployment:

- [ ] Copy deployment URL
- [ ] Test `/health` endpoint
- [ ] Test manual prediction
- [ ] Test batch upload
- [ ] Add deployment URL to assignment submission
- [ ] Add "quantic-grader" as GitHub collaborator
- [ ] Include deployment URL in demo video

---

## 📝 Deployment URL Template

For your submission, include:

```
Deployment URL: https://guardai-malware-detection.onrender.com
GitHub Repository: https://github.com/your-username/new-assignemnt
```

---

**Estimated Deployment Time:** 10-15 minutes  
**Cost:** Free tier available on all platforms  
**Recommended Platform:** Render (easiest setup with render.yaml)
