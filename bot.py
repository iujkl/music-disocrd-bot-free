import discord
from discord.ext import commands
import asyncio
import os
from typing import Optional
from config import DISCORD_TOKEN, COMMAND_PREFIX
from music_player import MusicPlayer, Song
from utils import is_valid_youtube_url, format_duration, truncate_text, safe_disconnect

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

# Load Opus library for voice support
def load_opus():
    try:
        # Force reload opus
        import ctypes
        import ctypes.util
        
        # Find opus library
        opus_path = ctypes.util.find_library('opus')
        if opus_path:
            print(f"Found opus at: {opus_path}")
            
        # Try multiple loading methods
        methods = ['libopus.so.0', 'libopus.so', 'opus']
        for method in methods:
            try:
                discord.opus.load_opus(method)
                print(f"Opus loaded successfully with: {method}")
                return True
            except Exception as e:
                print(f"Failed with {method}: {e}")
                continue
        
        print("All opus loading methods failed")
        return False
    except Exception as e:
        print(f"Error in opus loading: {e}")
        return False

load_opus()

# Create bot instance
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# Global music player instance
music_player = MusicPlayer(bot)

@bot.event
async def on_ready():
    """Event triggered when bot is ready."""
    print(f"{bot.user} has connected to Discord!")
    print(f"Bot is ready to play music!")
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=f"{COMMAND_PREFIX}musichelp | Music Bot"
        )
    )

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Unknown command. Use `{COMMAND_PREFIX}musichelp` for available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument. Use `{COMMAND_PREFIX}musichelp` for command usage.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ Invalid argument provided. Use `{COMMAND_PREFIX}musichelp` for command usage.")
    else:
        print(f"Command error: {error}")
        await ctx.send(f"❌ An error occurred while executing the command.")

@bot.command(name='join', aliases=['connect'])
async def join_voice_channel(ctx):
    """Join the voice channel of the user."""
    if not ctx.author.voice:
        await ctx.send("❌ You need to be in a voice channel to use this command!")
        return
    
    channel = ctx.author.voice.channel
    
    if music_player.voice_client and music_player.voice_client.is_connected():
        await music_player.voice_client.move_to(channel)
        await ctx.send(f"🔄 Moved to **{channel.name}**")
    else:
        music_player.voice_client = await channel.connect()
        await ctx.send(f"✅ Joined **{channel.name}**")

@bot.command(name='leave', aliases=['disconnect'])
async def leave_voice_channel(ctx):
    """Leave the current voice channel."""
    if not music_player.voice_client:
        await ctx.send("❌ Bot is not connected to a voice channel!")
        return
    
    await music_player.stop()
    await safe_disconnect(music_player.voice_client)
    music_player.voice_client = None
    await ctx.send("👋 Disconnected from voice channel!")

@bot.command(name='play', aliases=['p'])
async def play_music(ctx, *, query: str):
    """Play music from YouTube URL or search query."""
    # Check if user is in voice channel
    if not ctx.author.voice:
        await ctx.send("❌ You need to be in a voice channel to play music!")
        return
    
    # Join voice channel if not already connected
    if not music_player.voice_client or not music_player.voice_client.is_connected():
        await join_voice_channel(ctx)
        # Wait a moment for connection to stabilize
        await asyncio.sleep(1)
    
    # Show loading message
    loading_msg = await ctx.send("🔍 Searching for song...")
    
    # Extract song information
    song = await music_player.extract_song_info(query)
    
    if not song:
        await loading_msg.edit(content="❌ Could not find or load the requested song! This might be due to:\n• The video being DRM protected\n• The video being unavailable\n• Network issues\n\nTry searching for a different song or using a different YouTube video.")
        return
    
    # Set requester
    song.requester = ctx.author
    
    # Add to queue
    await music_player.add_to_queue(song)
    
    # Create embed for song info
    embed = discord.Embed(
        title="🎵 Song Added to Queue",
        description=f"**{song.title}**",
        color=discord.Color.green()
    )
    
    embed.add_field(name="Duration", value=format_duration(song.duration or 0), inline=True)
    embed.add_field(name="Requested by", value=song.requester.mention, inline=True)
    embed.add_field(name="Position in queue", value=len(music_player.queue), inline=True)
    
    if song.thumbnail:
        embed.set_thumbnail(url=song.thumbnail)
    
    await loading_msg.edit(content="", embed=embed)
    
    # Start playing if not already playing
    if not music_player.is_playing and music_player.voice_client and not music_player.voice_client.is_playing():
        await music_player.play_next()

@bot.command(name='pause')
async def pause_music(ctx):
    """Pause the current song."""
    if await music_player.pause():
        await ctx.send("⏸️ Music paused!")
    else:
        await ctx.send("❌ Nothing is currently playing!")

@bot.command(name='resume', aliases=['unpause'])
async def resume_music(ctx):
    """Resume the paused song."""
    if await music_player.resume():
        await ctx.send("▶️ Music resumed!")
    else:
        await ctx.send("❌ Music is not paused!")

@bot.command(name='stop')
async def stop_music(ctx):
    """Stop the music and clear the queue."""
    if await music_player.stop():
        await ctx.send("⏹️ Music stopped and queue cleared!")
    else:
        await ctx.send("❌ Nothing is currently playing!")

@bot.command(name='skip', aliases=['next'])
async def skip_song(ctx):
    """Skip the current song."""
    if await music_player.skip():
        await ctx.send("⏭️ Song skipped!")
    else:
        await ctx.send("❌ Nothing is currently playing!")

@bot.command(name='queue', aliases=['q'])
async def show_queue(ctx):
    """Show the current queue."""
    queue_info = music_player.get_queue_info()
    
    embed = discord.Embed(
        title="🎵 Music Queue",
        color=discord.Color.blue()
    )
    
    # Current song
    if queue_info['current_song']:
        current = queue_info['current_song']
        status = "⏸️ Paused" if queue_info['is_paused'] else "▶️ Playing"
        embed.add_field(
            name="Now Playing",
            value=f"{status} {current}",
            inline=False
        )
    else:
        embed.add_field(
            name="Now Playing",
            value="Nothing is currently playing",
            inline=False
        )
    
    # Queue
    if queue_info['queue']:
        queue_text = ""
        for i, song in enumerate(queue_info['queue'][:10], 1):  # Show first 10 songs
            queue_text += f"{i}. {song}\n"
        
        if len(queue_info['queue']) > 10:
            queue_text += f"... and {len(queue_info['queue']) - 10} more songs"
        
        embed.add_field(
            name=f"Up Next ({queue_info['queue_length']} songs)",
            value=queue_text,
            inline=False
        )
    else:
        embed.add_field(
            name="Up Next",
            value="Queue is empty",
            inline=False
        )
    
    # Volume
    embed.add_field(
        name="Volume",
        value=f"{int(queue_info['volume'] * 100)}%",
        inline=True
    )
    
    await ctx.send(embed=embed)

@bot.command(name='volume', aliases=['vol'])
async def set_volume(ctx, volume: int):
    """Set the volume (0-100)."""
    if not 0 <= volume <= 100:
        await ctx.send("❌ Volume must be between 0 and 100!")
        return
    
    volume_float = volume / 100.0
    
    if await music_player.set_volume(volume_float):
        await ctx.send(f"🔊 Volume set to {volume}%!")
    else:
        await ctx.send("❌ Could not set volume!")

@bot.command(name='nowplaying', aliases=['np'])
async def now_playing(ctx):
    """Show information about the currently playing song."""
    if not music_player.current_song:
        await ctx.send("❌ Nothing is currently playing!")
        return
    
    song = music_player.current_song
    
    embed = discord.Embed(
        title="🎵 Now Playing",
        description=f"**{song.title}**",
        color=discord.Color.green()
    )
    
    embed.add_field(name="Duration", value=format_duration(song.duration or 0), inline=True)
    embed.add_field(name="Requested by", value=song.requester.mention if song.requester else "Unknown", inline=True)
    embed.add_field(name="Volume", value=f"{int(music_player.volume * 100)}%", inline=True)
    
    status = "⏸️ Paused" if music_player.is_paused else "▶️ Playing"
    embed.add_field(name="Status", value=status, inline=True)
    
    if song.thumbnail:
        embed.set_thumbnail(url=song.thumbnail)
    
    await ctx.send(embed=embed)

@bot.command(name='clear')
async def clear_queue(ctx):
    """Clear the queue."""
    music_player.queue.clear()
    await ctx.send("🗑️ Queue cleared!")

@bot.command(name='musichelp', aliases=['commands'])
async def show_help(ctx):
    """Show help information."""
    embed = discord.Embed(
        title="🎵 Music Bot Commands",
        description="Here are all the available commands:",
        color=discord.Color.blue()
    )
    
    commands_list = [
        (f"`{COMMAND_PREFIX}play <song/url>`", "Play a song from YouTube"),
        (f"`{COMMAND_PREFIX}pause`", "Pause the current song"),
        (f"`{COMMAND_PREFIX}resume`", "Resume the paused song"),
        (f"`{COMMAND_PREFIX}stop`", "Stop music and clear queue"),
        (f"`{COMMAND_PREFIX}skip`", "Skip the current song"),
        (f"`{COMMAND_PREFIX}queue`", "Show the current queue"),
        (f"`{COMMAND_PREFIX}volume <0-100>`", "Set the volume"),
        (f"`{COMMAND_PREFIX}nowplaying`", "Show current song info"),
        (f"`{COMMAND_PREFIX}clear`", "Clear the queue"),
        (f"`{COMMAND_PREFIX}join`", "Join your voice channel"),
        (f"`{COMMAND_PREFIX}leave`", "Leave the voice channel"),
    ]
    
    for command, description in commands_list:
        embed.add_field(name=command, value=description, inline=False)
    
    embed.set_footer(text="🎵 Enjoy your music!")
    await ctx.send(embed=embed)

# Error handler for voice connection issues
@bot.event
async def on_voice_state_update(member, before, after):
    """Handle voice state updates."""
    # If bot is alone in channel, disconnect after 5 minutes
    if member == bot.user:
        return
    
    if music_player.voice_client and music_player.voice_client.channel:
        channel = music_player.voice_client.channel
        members = [m for m in channel.members if not m.bot]
        
        if len(members) == 0:
            await asyncio.sleep(300)  # Wait 5 minutes
            # Check again if still alone
            if music_player.voice_client and music_player.voice_client.channel:
                members = [m for m in music_player.voice_client.channel.members if not m.bot]
                if len(members) == 0:
                    await music_player.stop()
                    await safe_disconnect(music_player.voice_client)
                    music_player.voice_client = None

# Run the bot
if __name__ == "__main__":
    if DISCORD_TOKEN == "your_discord_bot_token_here":
        print("❌ Please set your Discord bot token in the DISCORD_TOKEN environment variable!")
        print("You can get a bot token from: https://discord.com/developers/applications")
    else:
        print("🤖 Starting Discord Music Bot...")
        bot.run(DISCORD_TOKEN)
