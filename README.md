# ProVision Brokerage AI Chatbot Demo

A professional AI-powered chatbot demo for ProVision Brokerage, showcasing multi-channel engagement and lead qualification capabilities.

## 🚀 Features

- **AI-Powered Chatbot**: Intelligent responses based on ProVision's knowledge base
- **Multi-Channel UI**: Website, SMS, WhatsApp, and Facebook integration previews
- **Lead Qualification**: Smart qualification questions and appointment booking
- **Coming Soon Pages**: Professional previews of upcoming features
- **Responsive Design**: Works on desktop and mobile devices

## 📁 Project Structure

```
├── frontend/
│   ├── index.html          # Main HTML file
│   └── runtime.jsx         # React components & UI
├── backend/
│   ├── main_ui_server.py   # FastAPI server
│   ├── intelligent_chatbot.py  # AI chatbot logic
│   └── requirements.txt    # Python dependencies
├── vercel.json            # Vercel configuration
├── package.json          # Node.js configuration
└── README.md             # This file
```

## 🛠️ Local Development

### Prerequisites
- Python 3.9+
- Node.js 14+

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main_ui_server.py
```

### Frontend Setup
```bash
# Serve the frontend files
python -m http.server 3000
```

## 🌐 Deployment

### Vercel Deployment
1. Connect your GitHub repository to Vercel
2. Vercel will automatically detect the configuration
3. Deploy with zero configuration

### Manual Deployment
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

## 🔧 Configuration

### Environment Variables
Set these in your Vercel dashboard:
- `OPENAI_API_KEY`: Your OpenAI API key

### API Endpoints
- `POST /api/chat`: Chat with the AI bot
- `GET /api/health`: Health check endpoint

## 📱 Demo Features

### Navigation Tabs
- **Seminars**: Seminar management system preview
- **Appointments**: Smart booking system preview  
- **Facebook**: Social media integration preview
- **Website Leads**: Lead management dashboard preview
- **Client Service**: Enhanced support system preview

### AI Chatbot
- Intelligent responses based on ProVision's knowledge
- Age-appropriate retirement advice
- Sales-focused conversation flow
- Multi-channel simulation

## 🎯 Demo Use Cases

1. **Lead Qualification**: Ask about retirement planning
2. **Age-Specific Advice**: Test responses for different age groups
3. **Feature Previews**: Navigate through "Coming Soon" pages
4. **Multi-Channel**: Experience different communication channels

## 📞 Support

For technical support or questions about the demo, please contact the development team.

---

**ProVision Brokerage** - AI-Powered Lead Management Demo
