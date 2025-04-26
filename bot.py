import os
import logging
from typing import Dict, List
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from pytube import YouTube
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import (
    TELEGRAM_TOKEN,
    YOUTUBE_API_KEY_VALUE,
    PORT,
    DOMAIN,
    MAX_VIDEO_SIZE
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY_VALUE)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Welcome! I can help you search and download YouTube videos.\n'
        'Use /search <query> to search for videos\n'
        'Use /download <url> to download a video'
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Search YouTube and return results."""
    if not context.args:
        await update.message.reply_text('Please provide a search query.')
        return

    query = ' '.join(context.args)
    try:
        # Search YouTube
        search_response = youtube.search().list(
            q=query,
            part='snippet',
            maxResults=10,
            type='video'
        ).execute()

        if not search_response['items']:
            await update.message.reply_text('No videos found.')
            return

        # Create inline keyboard with video options
        keyboard = []
        for idx, item in enumerate(search_response['items'], 1):
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            keyboard.append([
                InlineKeyboardButton(
                    f"{idx}. {title[:50]}...",
                    callback_data=f"video_{video_id}"
                )
            ])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            'Here are the top 10 results. Click on a video to get its link:',
            reply_markup=reply_markup
        )

    except HttpError as e:
        logger.error(f"An HTTP error occurred: {e}")
        await update.message.reply_text('Sorry, there was an error searching YouTube.')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()

    if query.data.startswith('video_'):
        video_id = query.data.split('_')[1]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        await query.message.reply_text(f"Here's the video link: {video_url}")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Download and send a YouTube video."""
    if not context.args:
        await update.message.reply_text('Please provide a YouTube URL.')
        return

    url = context.args[0]
    try:
        # Download video
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        if not video:
            await update.message.reply_text('No suitable video stream found.')
            return

        # Check file size
        if video.filesize > MAX_VIDEO_SIZE:
            await update.message.reply_text(
                'Sorry, this video is too large to send through Telegram (max 50MB).'
            )
            return

        # Download and send
        await update.message.reply_text('Downloading video...')
        video_path = video.download()
        
        with open(video_path, 'rb') as video_file:
            await update.message.reply_video(
                video=video_file,
                caption=f"Here's your video: {yt.title}"
            )
        
        # Clean up
        os.remove(video_path)

    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        await update.message.reply_text('Sorry, there was an error downloading the video.')

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(CommandHandler("download", download))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start the Bot
    application.run_webhook(
        listen='0.0.0.0',
        port=PORT,
        url_path=TELEGRAM_TOKEN,
        webhook_url=f"https://{DOMAIN}/{TELEGRAM_TOKEN}"
    )

if __name__ == '__main__':
    main() 