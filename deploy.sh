#!/bin/bash

# ProVision Brokerage Demo Deployment Script

echo "🚀 Deploying ProVision Brokerage Demo to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Deploy to Vercel
echo "📦 Building and deploying..."
vercel --prod

echo "✅ Deployment complete!"
echo "🌐 Your demo is now live on Vercel!"
