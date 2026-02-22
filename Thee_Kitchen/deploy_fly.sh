#!/bin/bash

# Deploy Thee Kitchen to Fly.io
echo "🚀 Deploying Thee Kitchen to Fly.io..."

# Check if Fly CLI is installed
if ! command -v fly &> /dev/null; then
    echo "❌ Fly CLI not found. Installing..."
    curl -L https://fly.io/install.sh | sh
    export PATH="$HOME/.fly/bin:$PATH"
fi

# Login to Fly (if not already logged in)
echo "🔐 Checking Fly authentication..."
if ! fly auth whoami &> /dev/null; then
    echo "Please login to Fly.io:"
    echo "1. Visit: https://fly.io/app/sign-up"
    echo "2. After signup, run: fly auth login"
    exit 1
fi

# Deploy to Fly.io
echo "📦 Deploying application..."
fly deploy

echo "✅ Deployment complete!"
echo "🌐 Your app is available at: https://thee-kitchen.fly.dev"
