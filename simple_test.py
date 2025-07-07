#!/usr/bin/env python3
import discord
import asyncio
import os

# Force load opus
try:
    import ctypes
    import ctypes.util
    
    # Try to find and load opus library directly
    opus_lib = ctypes.util.find_library('opus')
    if opus_lib:
        print(f"Found opus library at: {opus_lib}")
        discord.opus._lib = ctypes.CDLL(opus_lib)
        print("Opus loaded directly!")
    else:
        print("Opus library not found")
        
    # Alternative loading
    if not discord.opus.is_loaded():
        discord.opus.load_opus('libopus.so.0')
        
except Exception as e:
    print(f"Error loading opus: {e}")

print(f"Opus loaded: {discord.opus.is_loaded()}")

# Simple bot test
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

class SimpleBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        
    async def on_ready(self):
        print(f'Simple bot ready: {self.user}')
        print(f'Opus status: {discord.opus.is_loaded()}')

# Test if this helps
if __name__ == "__main__":
    print("Testing simplified Discord setup...")