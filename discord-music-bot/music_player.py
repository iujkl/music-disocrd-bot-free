import asyncio
import discord
from discord.ext import commands
import yt_dlp
from typing import Optional, List, Dict, Any
import json
from config import YTDL_OPTIONS, FFMPEG_OPTIONS, DEFAULT_VOLUME
from utils import is_valid_youtube_url, format_duration, truncate_text

class Song:
    """Represents a song with metadata."""
    
    def __init__(self, title: str, url: str, duration: Optional[int] = None, 
                 thumbnail: Optional[str] = None, requester: Optional[discord.Member] = None):
        self.title = title
        self.url = url
        self.duration = duration
        self.thumbnail = thumbnail
        self.requester = requester
        self.stream_url = None
        
    def __str__(self) -> str:
        duration_str = format_duration(self.duration) if self.duration else "Unknown"
        return f"**{truncate_text(self.title)}** [{duration_str}]"

class MusicPlayer:
    """Main music player class handling queue and playback."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queue: List[Song] = []
        self.current_song: Optional[Song] = None
        self.voice_client: Optional[discord.VoiceClient] = None
        self.volume = DEFAULT_VOLUME
        self.is_playing = False
        self.is_paused = False
        self.loop_enabled = False
        self.ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)
        
    async def extract_song_info(self, query: str) -> Optional[Song]:
        """
        Extract song information from YouTube URL or search query.
        
        Args:
            query (str): YouTube URL or search query
            
        Returns:
            Optional[Song]: Song object if successful, None otherwise
        """
        try:
            # Run yt-dlp extraction in executor to avoid blocking
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(query, download=False))
            
            if not data:
                return None
                
            # Handle playlist - take first entry
            if 'entries' in data and data['entries']:
                data = data['entries'][0]
            
            title = data.get('title', 'Unknown Title')
            url = data.get('webpage_url', query)
            duration = data.get('duration')
            thumbnail = data.get('thumbnail')
            
            song = Song(title, url, duration, thumbnail)
            song.stream_url = data.get('url')
            
            return song
            
        except Exception as e:
            print(f"Error extracting song info: {e}")
            # Return None with error info for better user feedback
            return None
    
    async def add_to_queue(self, song: Song) -> None:
        """Add a song to the queue."""
        self.queue.append(song)
        
    async def play_next(self) -> None:
        """Play the next song in the queue."""
        if not self.queue:
            self.is_playing = False
            self.current_song = None
            # Disconnect after 5 minutes of inactivity
            await asyncio.sleep(300)
            if not self.is_playing and self.voice_client:
                await self.voice_client.disconnect()
            return
            
        if self.voice_client and not self.voice_client.is_connected():
            return
            
        self.current_song = self.queue.pop(0)
        
        # Get fresh stream URL
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                None, 
                lambda: self.ytdl.extract_info(self.current_song.url, download=False)
            )
            
            if data and 'entries' in data and data['entries']:
                data = data['entries'][0]
                
            if not data:
                await self.play_next()
                return
                
            stream_url = data.get('url')
            if not stream_url:
                await self.play_next()
                return
                
        except Exception as e:
            print(f"Error getting stream URL: {e}")
            await self.play_next()
            return
        
        # Create audio source
        try:
            print(f"Attempting to play stream URL: {stream_url}")
            
            # Create the audio source with proper error handling
            audio_source = discord.FFmpegPCMAudio(
                stream_url, 
                before_options=FFMPEG_OPTIONS['before_options'],
                options=FFMPEG_OPTIONS['options']
            )
            
            print("Audio source created successfully")
            
            # Wrap with volume transformer
            audio_source = discord.PCMVolumeTransformer(audio_source, volume=self.volume)
            
            print("Volume transformer applied")
            
            # Play the audio
            if self.voice_client:
                print("Starting playback...")
                self.voice_client.play(audio_source, after=lambda e: self.handle_playback_error(e))
                self.is_playing = True
                self.is_paused = False
                print("Playback started successfully")
            else:
                print("No voice client available")
            
        except Exception as e:
            print(f"Error playing audio: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            traceback.print_exc()
            await self.play_next()
    
    def handle_playback_error(self, error) -> None:
        """Handle playback errors and continue to next song."""
        if error:
            print(f"Playback error: {error}")
        else:
            print("Song finished playing")
        
        # Reset playing state
        self.is_playing = False
        self.is_paused = False
        
        # Schedule next song
        asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop)
    
    async def pause(self) -> bool:
        """Pause the current song."""
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.pause()
            self.is_paused = True
            return True
        return False
    
    async def resume(self) -> bool:
        """Resume the paused song."""
        if self.voice_client and self.voice_client.is_paused():
            self.voice_client.resume()
            self.is_paused = False
            return True
        return False
    
    async def stop(self) -> bool:
        """Stop the current song and clear queue."""
        if self.voice_client and (self.voice_client.is_playing() or self.voice_client.is_paused()):
            self.voice_client.stop()
            self.queue.clear()
            self.current_song = None
            self.is_playing = False
            self.is_paused = False
            return True
        return False
    
    async def skip(self) -> bool:
        """Skip the current song."""
        if self.voice_client and (self.voice_client.is_playing() or self.voice_client.is_paused()):
            self.voice_client.stop()
            return True
        return False
    
    async def set_volume(self, volume: float) -> bool:
        """Set the volume (0.0 to 1.0)."""
        if 0.0 <= volume <= 1.0:
            self.volume = volume
            if self.voice_client and hasattr(self.voice_client.source, 'volume'):
                self.voice_client.source.volume = volume
            return True
        return False
    
    def get_queue_info(self) -> Dict[str, Any]:
        """Get current queue information."""
        return {
            'current_song': self.current_song,
            'queue': self.queue,
            'is_playing': self.is_playing,
            'is_paused': self.is_paused,
            'volume': self.volume,
            'queue_length': len(self.queue)
        }
