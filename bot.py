# bot.py
import os
import json
from random import randrange

import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
MY_ID: int = os.getenv('USER_ID')
EMOTE = os.getenv('EMOTE_RESPONSE')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents = intents, command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Adds a specific reaction to every message I send, but no one else.
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.author.id == MY_ID:
        await message.add_reaction(EMOTE)
    
    await bot.process_commands(message)

@bot.command()
async def fun_facts(ctx, command = '', fact = ''):
    command = command.lower()

    # Ensures a file is created if it doesn't already exist
    file_path = 'funfacts.json'
    if not os.path.exists('file_path'):
        with open(file_path, 'w') as file:
            data = { "facts": [] }
            json.dump(data, file)

    match command:
        case '':
            with open('funfacts.json', 'r') as file:
                data = json.load(file)
                if (len(data['facts']) != 0):
                    randomizer = randrange(len(data['facts']))
                    await ctx.send(data['facts'][randomizer]['fact'])
                else:
                    await ctx.send("There are no fun facts to be had. :(")
               
        case 'add':
            with open('funfacts.json', 'r+') as file:
                if (len(fact) > 5):
                    data = json.load(file)
                    new_fact = {"id": (len(data['facts']) + 1),
                                "fact": fact
                                }
                    data['facts'].append(new_fact)
                    file.seek(0)
                    json.dump(data, file, indent = 4)
                    await ctx.send(f'Your fact was added.')
                elif ((len(fact) < 8) & (fact != '')):
                    await ctx.send("What kind of fact is less than 8 characters? Are you dumb? I'm not adding that.")
                else:
                    await ctx.send("You didn't enter a fact. I won't add nothing, that's impossible!")
        case _:
            await ctx.send('Invalid command.')


            

bot.run(TOKEN)