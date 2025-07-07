# Discord Bot Setup Guide

## Step 1: Create Bot Application
1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Give your bot a name (e.g., "Music Bot")
4. Click "Create"

## Step 2: Create Bot User
1. Go to "Bot" section in left sidebar
2. Click "Add Bot"
3. Copy the token and add it to your Replit secrets as DISCORD_TOKEN

## Step 3: Set Bot Permissions
In the Bot section, enable these permissions:
- Send Messages
- Use Slash Commands
- Connect (to voice channels)
- Speak (in voice channels)
- Use Voice Activity

## Step 4: Generate Invite Link
1. Go to "OAuth2" > "URL Generator"
2. Select "bot" in Scopes
3. Select these Bot Permissions:
   - Send Messages ✓
   - Read Message History ✓
   - Connect ✓
   - Speak ✓
   - Use Voice Activity ✓
4. Copy the generated URL
5. Visit the URL to invite your bot to your server

## Step 5: Test Bot
1. Join a voice channel in your Discord server
2. Type: !play never gonna give you up
3. Bot should join and play music

## Common Issues:
- Bot needs to be invited with proper voice permissions
- Make sure you're in a voice channel before using !play
- Bot token must be correctly set in Replit secrets