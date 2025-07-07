# Discord Music Bot - VS Code Setup

## Quick Start:

1. Install Python 3.11+ and VS Code
2. Open this folder in VS Code
3. Install Python extension in VS Code
4. Open terminal in VS Code and run:

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # Mac/Linux

pip install discord.py yt-dlp PyNaCl python-dotenv
```

5. Copy .env.example to .env and add your Discord bot token
6. Install FFmpeg on your system
7. Press F5 to run the bot in debug mode

## Commands:
- !play <song> - Play music
- !pause - Pause music  
- !resume - Resume music
- !skip - Skip song
- !queue - Show queue
- !volume <0-100> - Set volume
- !musichelp - Show all commands

Your bot is ready to use!
