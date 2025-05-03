# bot.py
import os

import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
MY_ID = os.getenv('USER_ID')
EMOTE = os.getenv('EMOTE_RESPONSE')

bot = commands.Bot(intents=discord.Intents.default(), command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Adds a specific reaction to every message I send, but no one else.
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.author.id == int(MY_ID):
        await message.add_reaction(EMOTE)

bot.run(TOKEN)