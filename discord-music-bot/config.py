import os

# Try to load environment variables from .env file (for Visual Studio development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, use system environment variables
    pass

# Discord bot token from environment variable
DISCORD_TOKEN = os.getenv("MTM5MTUzNTQ2OTk2NzQ0NjEwNg.Gda8yR.mjv0B_KpQIg3dv19fCEioOffi_R0hLaTuGknr0", "your_discord_bot_token_here")

# Bot command prefix
COMMAND_PREFIX = "!"

# YouTube DLP options for audio extraction
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'logtostderr': False,
    'ignoreerrors': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

# FFmpeg options for audio streaming
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -filter:a "volume=0.25"'
}

# Default volume (0.0 to 1.0)
DEFAULT_VOLUME = 0.5
