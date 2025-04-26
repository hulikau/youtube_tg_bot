"""
Environment variable keys used throughout the application.
This file serves as a single source of truth for all environment variable names.
"""

# Telegram Bot Configuration
TELEGRAM_TOKEN_KEY = 'TELEGRAM_TOKEN'

# YouTube API Configuration
YOUTUBE_API_KEY = 'YOUTUBE_API_KEY'

# Server Configuration
PORT_KEY = 'PORT'
DOMAIN_KEY = 'DOMAIN'

# Google Cloud Configuration
REGION_KEY = 'REGION'
PROJECT_ID_KEY = 'PROJECT_ID'

# Default Values
DEFAULT_PORT = '8080'
DEFAULT_REGION = 'us-central1'

# Constants
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB Telegram limit 