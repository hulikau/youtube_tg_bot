#!/bin/bash

# Exit on error
set -e

# Load environment variables from .env file
if [ -f .env ]; then
    source .env
else
    echo "Error: .env file not found"
    exit 1
fi

# Check if required environment variables are set
if [ -z "$TELEGRAM_TOKEN" ] || [ -z "$YOUTUBE_API_KEY" ] || [ -z "$DOMAIN" ]; then
    echo "Error: TELEGRAM_TOKEN, YOUTUBE_API_KEY, and DOMAIN must be set in .env file"
    exit 1
fi

# Get the current project ID if not set
if [ -z "$PROJECT_ID" ]; then
    PROJECT_ID=$(gcloud config get-value project)
    if [ -z "$PROJECT_ID" ]; then
        echo "Error: No Google Cloud project ID found. Please set PROJECT_ID in .env or run 'gcloud config set project [PROJECT_ID]'"
        exit 1
    fi
fi

# Set default region if not provided
REGION=${REGION:-"us-central1"}

# Build the Docker image
echo "Building Docker image..."
docker build -t youtube-telegram-bot .

# Tag the image for Google Container Registry
echo "Tagging image for GCR..."
docker tag youtube-telegram-bot gcr.io/$PROJECT_ID/youtube-telegram-bot

# Push the image to Google Container Registry
echo "Pushing image to GCR..."
docker push gcr.io/$PROJECT_ID/youtube-telegram-bot

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy youtube-telegram-bot \
    --image gcr.io/$PROJECT_ID/youtube-telegram-bot \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars="TELEGRAM_TOKEN=$TELEGRAM_TOKEN,YOUTUBE_API_KEY=$YOUTUBE_API_KEY,DOMAIN=$DOMAIN"

# Get the service URL
SERVICE_URL=$(gcloud run services describe youtube-telegram-bot --platform managed --region $REGION --format 'value(status.url)')

# Set up the webhook
echo "Setting up webhook..."
curl -F "url=$SERVICE_URL/$TELEGRAM_TOKEN" \
    https://api.telegram.org/bot$TELEGRAM_TOKEN/setWebhook

echo "Deployment completed successfully!"
echo "Service URL: $SERVICE_URL" 