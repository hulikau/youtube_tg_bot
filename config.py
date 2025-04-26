import os
from dotenv import load_dotenv
from env_keys import (
    TELEGRAM_TOKEN_KEY,
    YOUTUBE_API_KEY,
    PORT_KEY,
    DOMAIN_KEY,
    REGION_KEY,
    PROJECT_ID_KEY,
    DEFAULT_PORT,
    DEFAULT_REGION,
    MAX_VIDEO_SIZE
)

# Load environment variables from both .env and .secret files
load_dotenv('.env')
load_dotenv('.secret', override=True)  # .secret values override .env values

# Telegram Bot Configuration
TELEGRAM_TOKEN = os.getenv(TELEGRAM_TOKEN_KEY)
if not TELEGRAM_TOKEN:
    raise ValueError(f"{TELEGRAM_TOKEN_KEY} environment variable is not set")

# YouTube API Configuration
YOUTUBE_API_KEY_VALUE = os.getenv(YOUTUBE_API_KEY)
if not YOUTUBE_API_KEY_VALUE:
    raise ValueError(f"{YOUTUBE_API_KEY} environment variable is not set")

# Server Configuration
PORT = int(os.getenv(PORT_KEY, DEFAULT_PORT))
DOMAIN = os.getenv(DOMAIN_KEY)
if not DOMAIN:
    raise ValueError(f"{DOMAIN_KEY} environment variable is not set")

# Google Cloud Configuration
REGION = os.getenv(REGION_KEY, DEFAULT_REGION)
PROJECT_ID = os.getenv(PROJECT_ID_KEY)

# Export constants
__all__ = [
    'TELEGRAM_TOKEN',
    'YOUTUBE_API_KEY_VALUE',
    'PORT',
    'DOMAIN',
    'REGION',
    'PROJECT_ID',
    'MAX_VIDEO_SIZE'
] 