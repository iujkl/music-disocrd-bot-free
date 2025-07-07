#!/usr/bin/env python3
"""
Script to prepare Discord Music Bot files for Visual Studio setup
Run this script to create all necessary files for local development
"""

import os
import shutil

def create_vs_project():
    """Create a Visual Studio-ready project structure"""
    
    # Create project directory
    project_name = "discord-music-bot"
    if os.path.exists(project_name):
        print(f"Directory {project_name} already exists!")
        return
    
    os.makedirs(project_name)
    os.makedirs(f"{project_name}/.vscode")
    
    # Files to copy
    files_to_copy = [
        "bot.py",
        "config.py", 
        "music_player.py",
        "utils.py",
        "packages.txt",
        ".env.example"
    ]
    
    # Copy files
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, f"{project_name}/{file}")
            print(f"Copied {file}")
    
    # Create VS Code settings
    vscode_settings = """{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true
}"""
    
    with open(f"{project_name}/.vscode/settings.json", "w") as f:
        f.write(vscode_settings)
    
    # Create launch configuration
    launch_config = """{
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
}"""
    
    with open(f"{project_name}/.vscode/launch.json", "w") as f:
        f.write(launch_config)
    
    # Create setup instructions
    setup_instructions = """# Discord Music Bot - VS Code Setup

## Quick Start:

1. Install Python 3.11+ and VS Code
2. Open this folder in VS Code
3. Install Python extension in VS Code
4. Open terminal in VS Code and run:

```bash
python -m venv venv
venv\\Scripts\\activate   # Windows
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
"""
    
    with open(f"{project_name}/README.md", "w") as f:
        f.write(setup_instructions)
    
    print(f"\n✅ Project '{project_name}' created successfully!")
    print(f"📁 Open the '{project_name}' folder in Visual Studio Code")
    print("📋 Follow the README.md instructions to set up your environment")

if __name__ == "__main__":
    create_vs_project()