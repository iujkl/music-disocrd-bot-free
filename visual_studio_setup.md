# Using Discord Music Bot in Visual Studio

## Prerequisites
1. **Python Extension**: Install Python extension for VS Code
2. **Python 3.11+**: Make sure Python is installed on your system
3. **Git**: For version control (optional)

## Setup Steps

### 1. Create New Project
```bash
mkdir discord-music-bot
cd discord-music-bot
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Required Packages
```bash
pip install discord.py yt-dlp PyNaCl
```

### 4. Install FFmpeg
**Windows:**
- Download from https://ffmpeg.org/download.html
- Add to PATH environment variable

**Mac:**
```bash
brew install ffmpeg opus
```

**Linux:**
```bash
sudo apt install ffmpeg libopus0
```

### 5. Project Structure
```
discord-music-bot/
├── bot.py              # Main bot file
├── config.py           # Configuration settings
├── music_player.py     # Music player logic
├── utils.py            # Utility functions
├── requirements.txt    # Package dependencies
└── .env               # Environment variables (create this)
```

### 6. Environment Variables
Create `.env` file:
```
DISCORD_TOKEN=your_bot_token_here
```

### 7. VS Code Configuration
Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true
}
```

### 8. Requirements File
Create `requirements.txt`:
```
discord.py>=2.5.2
yt-dlp>=2025.6.30
PyNaCl>=1.5.0
python-dotenv>=1.0.0
```

## Running the Bot

### In VS Code Terminal:
```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

# Run the bot
python bot.py
```

## VS Code Extensions (Recommended)
- Python
- Python Debugger
- GitLens
- Error Lens

## Debugging Setup
Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Discord Bot",
            "type": "python",
            "request": "launch",
            "program": "bot.py",
            "console": "integratedTerminal",
            "envFile": "${workspaceFolder}/.env"
        }
    ]
}
```