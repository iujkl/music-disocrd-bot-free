# Discord Music Bot

## Overview

This is a Discord music bot built with Python that allows users to play music in voice channels. The bot uses discord.py for Discord integration and yt-dlp for YouTube audio extraction. It features a command-based interface with music queue management, playback controls, and basic user interaction.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **bot.py**: Main bot entry point and command handlers
- **music_player.py**: Core music playback logic and queue management
- **config.py**: Configuration management and environment settings
- **utils.py**: Utility functions for URL validation, formatting, and text processing

The bot uses an event-driven architecture provided by discord.py, handling Discord events and user commands asynchronously.

## Key Components

### Discord Bot Core
- **Framework**: discord.py with command extensions
- **Intents**: Message content and voice state tracking enabled
- **Command Prefix**: Configurable (default: "!")
- **Error Handling**: Centralized command error management

### Music Player Engine
- **Audio Source**: YouTube via yt-dlp
- **Queue System**: FIFO queue with Song objects
- **Playback Control**: Play, pause, skip, loop functionality
- **Volume Control**: Adjustable audio levels (0.0 to 1.0)

### Song Management
- **Song Class**: Encapsulates track metadata (title, URL, duration, thumbnail, requester)
- **Stream Handling**: Dynamic URL resolution for audio streaming
- **Metadata Extraction**: Automatic song information retrieval

### Utility Functions
- **URL Validation**: YouTube URL pattern matching
- **Duration Formatting**: Human-readable time display
- **Text Processing**: Content truncation for Discord message limits

## Data Flow

1. **User Input**: Commands received via Discord messages
2. **Command Processing**: Bot parses and validates commands
3. **Music Request**: URLs or search queries processed by music player
4. **Metadata Extraction**: yt-dlp extracts song information
5. **Queue Management**: Songs added to playback queue
6. **Audio Streaming**: FFmpeg streams audio to Discord voice channel
7. **User Feedback**: Status updates sent to Discord text channel

## External Dependencies

### Core Dependencies
- **discord.py**: Discord API integration
- **yt-dlp**: YouTube audio extraction and metadata
- **FFmpeg**: Audio processing and streaming
- **asyncio**: Asynchronous programming support

### Configuration Requirements
- **Discord Bot Token**: Required environment variable
- **YouTube DLP Options**: Audio quality and extraction settings
- **FFmpeg Options**: Streaming optimization parameters

## Deployment Strategy

The bot is designed for simple deployment with minimal configuration:

1. **Environment Setup**: Discord bot token via environment variable
2. **Dependency Installation**: Python packages via pip
3. **System Requirements**: FFmpeg binary for audio processing
4. **Bot Permissions**: Voice channel access and message sending rights

The application follows a single-process model suitable for small to medium Discord servers.

## Changelog

```
Changelog:
- July 07, 2025. Initial setup
- July 07, 2025. Bot successfully deployed and running with Discord token
- July 07, 2025. Added FFmpeg system dependency for audio processing
- July 07, 2025. Improved error handling for DRM-protected content
- July 07, 2025. Fixed Opus codec loading - music now plays successfully
- July 07, 2025. Created Visual Studio Code setup files and documentation
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```

## Technical Notes

- The bot uses OAuth2 with Discord's bot framework for authentication
- Audio processing relies on FFmpeg with reconnection capabilities
- The music player supports single-server operation (one voice channel at a time)
- Error handling includes graceful degradation for network issues
- The codebase appears to be incomplete, with truncated files suggesting additional functionality

## Security Considerations

- Bot token stored as environment variable for security
- No user data persistence or storage
- Limited to Discord's built-in permission system
- YouTube content filtered through yt-dlp's safety mechanisms