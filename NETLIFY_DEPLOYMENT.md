# Netlify Deployment Guide for ProVision Brokerage

## 🚀 Quick Deployment Steps

### 1. Connect to Netlify
1. Go to [netlify.com](https://netlify.com)
2. Sign up/Login with GitHub
3. Click "New site from Git"
4. Choose your repository: `Nishanth2501/provision-brokerage`

### 2. Configure Build Settings
- **Build command**: Leave empty (no build needed)
- **Publish directory**: `frontend`
- **Functions directory**: `backend`

### 3. Set Environment Variables
In Netlify dashboard → Site settings → Environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key

### 4. Deploy!
Click "Deploy site" and you're done!

## 📁 Project Structure for Netlify

```
├── frontend/                    # Static site files
│   ├── index.html              # Main HTML file
│   └── runtime.jsx             # React components
├── backend/                    # Netlify Functions
│   ├── main_ui_server_netlify.py  # Netlify function
│   ├── intelligent_chatbot.py     # AI chatbot logic
│   └── requirements_netlify.txt   # Python dependencies
├── netlify.toml                # Netlify configuration
└── README.md
```

## 🔧 Configuration Files

### netlify.toml
- Configures redirects from `/api/*` to Netlify functions
- Sets up CORS for API calls
- Publishes frontend directory

### Backend Function
- `main_ui_server_netlify.py` - Netlify-compatible function
- Handles CORS and API routing
- Uses your existing chatbot logic

## 🌐 After Deployment

Your demo will be available at:
- **Main site**: `https://your-site-name.netlify.app`
- **API endpoint**: `https://your-site-name.netlify.app/api/chat`

## ✅ Features Working

- ✅ AI Chatbot with intelligent responses
- ✅ Multi-channel UI simulation
- ✅ Coming Soon pages for all tabs
- ✅ Responsive design
- ✅ Lead qualification flow
- ✅ Age-appropriate retirement advice

## 🎯 Demo Ready!

Your ProVision Brokerage demo is now live and ready to showcase to Eric and the team!
