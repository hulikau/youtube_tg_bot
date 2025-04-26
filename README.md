# YouTube Telegram Bot

A Telegram bot that allows users to search and download YouTube videos.

## Features

- `/search <query>`: Search YouTube and get top 10 results
- `/download <url>`: Download and send YouTube videos
- Interactive video selection
- File size limit handling
- Error handling and logging

## Prerequisites

- Python 3.11+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- YouTube Data API Key (from [Google Cloud Console](https://console.cloud.google.com))
- Google Cloud account (for deployment)

## Security Note

This project uses environment variables for sensitive configuration. Never commit your `.env` or `.secret` files to version control. The `.gitignore` file is configured to prevent accidental commits of sensitive data.

## Local Development Setup

1. Clone the repository
2. Create a `.env` file with the following variables (DO NOT commit this file):
   ```
   # Server Configuration
   PORT=8080
   DOMAIN=your-cloud-run-domain.com

   # Google Cloud Configuration
   REGION=us-central1
   PROJECT_ID=your-gcp-project-id
   ```

3. Create a `.secret` file with your API keys (DO NOT commit this file):
   ```
   # Telegram Bot Configuration
   TELEGRAM_TOKEN=your_telegram_bot_token_here

   # YouTube API Configuration
   YOUTUBE_API_KEY=your_youtube_api_key_here
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the bot:
   ```bash
   python bot.py
   ```

## Deployment to Google Cloud Run

1. Make sure your `.env` and `.secret` files are properly configured with all required variables
2. Run the deployment script:
   ```bash
   ./deploy.sh
   ```

The deployment script will:
- Build the Docker image
- Push it to Google Container Registry
- Deploy to Cloud Run
- Set up the webhook

## Environment Variables

The following environment variables are required:

### API Keys (in .secret)
- `TELEGRAM_TOKEN`: Your Telegram bot token
- `YOUTUBE_API_KEY`: Your YouTube Data API key

### Configuration (in .env)
- `PORT`: Port to run the webhook server (default: 8080)
- `DOMAIN`: Your Cloud Run service domain
- `REGION`: Google Cloud region (default: us-central1)
- `PROJECT_ID`: Your Google Cloud project ID

## Security Best Practices

1. Never commit `.env` or `.secret` files to version control
2. Use different API keys for development and production
3. Regularly rotate your API keys
4. Use environment variables for all sensitive configuration
5. Keep your dependencies up to date
6. Store API keys in `.secret` file and other configuration in `.env`

## Limitations

- Maximum video size: 50MB (Telegram limit)
- YouTube API quota limits apply
- Cloud Run timeout limits apply

## License

MIT
