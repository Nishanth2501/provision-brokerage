# Render Deployment Guide for ProVision Brokerage

## 🚀 Quick Deployment Steps

### 1. Connect to Render
1. Go to [render.com](https://render.com)
2. Sign up/Login with GitHub
3. Click "New +" → "Web Service"
4. Connect your repository: `Nishanth2501/provision-brokerage`

### 2. Configure Web Service
- **Name**: `provision-brokerage-demo`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `cd backend && python main_ui_server.py`
- **Publish Directory**: `frontend` (for static files)

### 3. Set Environment Variables
In Render dashboard → Environment:
- `OPENAI_API_KEY`: Your OpenAI API key

### 4. Deploy!
Click "Create Web Service" and you're done!

## 📁 Project Structure for Render

```
provision-brokerage/
├── frontend/                    # Static site files
│   ├── index.html              # Main HTML file
│   └── runtime.jsx             # React components
├── backend/                    # Python backend
│   ├── main_ui_server.py       # FastAPI server
│   ├── intelligent_chatbot.py  # AI chatbot logic
│   ├── start.py                # Render start script
│   └── requirements.txt        # Python dependencies
├── render.yaml                 # Render configuration
└── README.md
```

## 🔧 Configuration Files

### render.yaml
- Configures the web service
- Sets build and start commands
- Defines environment variables

### Backend Server
- `main_ui_server.py` - FastAPI server with CORS
- `intelligent_chatbot.py` - AI chatbot logic
- `start.py` - Render-compatible start script

## 🌐 After Deployment

Your demo will be available at:
- **Main site**: `https://your-service-name.onrender.com`
- **API endpoint**: `https://your-service-name.onrender.com/api/chat`

## ✅ Features Working

- ✅ AI Chatbot with intelligent responses
- ✅ Multi-channel UI simulation
- ✅ Coming Soon pages for all tabs
- ✅ Responsive design
- ✅ Lead qualification flow
- ✅ Age-appropriate retirement advice

## 🎯 Render Advantages

- **Free tier available**
- **Automatic deployments** from GitHub
- **Easy environment variable management**
- **Built-in HTTPS**
- **Automatic scaling**
- **Great Python support**

## 🚀 Demo Ready!

Your ProVision Brokerage demo is now ready for Render deployment!
