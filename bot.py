# bot.py
import os
import json
from random import randrange
import gamble
import fun_fact
import wow_stuff

import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
MY_ID = os.getenv('USER_ID')
EMOTE = os.getenv('EMOTE_RESPONSE')
SERVER_ID = os.getenv('SERVER_ID')
ROLE_ID = os.getenv('ROLE_ID')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(intents = intents, command_prefix='!', case_insensitive = True)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Adds a specific reaction to every message I send, but no one else.
@bot.event
async def on_message(message):
    if message.author.id == int(MY_ID):
        await message.add_reaction(EMOTE)
    
    await bot.process_commands(message)

@bot.command(name = 'fun-facts', description = "Have the bot print out a fun fact for everyone to enjoy, or edit the list yourself!")
async def fun_facts(ctx, command = commands.parameter(description = "Available commands: none, 'get', 'add', or 'remove'.", default = ''), value = commands.parameter(description = "Add = quotes, Get = integers, Remove = integers", default = '')):
    command = command.lower()
    guild_id = ctx.guild.id

    folder_path = 'fun_facts'
    # Ensures the file being opened is relative to the server it's being called from
    file_path = (f'{folder_path}/{guild_id}funfacts.json')

    pseudo_path = (f'{folder_path}/{guild_id}pseudorandom.json')

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    # Ensures a file is created if it doesn't already exist
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            data = { "facts": [] }
            json.dump(data, file, indent = 4)
    
    # Creates the file to help pseudo-randomize the fun facts
    if not os.path.exists(pseudo_path):
        with open(pseudo_path, 'w') as file:
            data = { "facts": [] }
            json.dump(data, file, indent = 4)

    match command:
        # Print random fact
        case '':
            await fun_fact.random_fact(file_path, ctx, pseudo_path)
        # Print fact based on given ID
        case 'get':
            await fun_fact.specific_fact(file_path, ctx, value, pseudo_path)
        # Add a fact to the list
        case 'add':
            await fun_fact.add_fact(file_path, pseudo_path, ctx, value)
        # Remove a fact from the list
        case 'remove':
            await fun_fact.remove_fact(file_path, ctx, value)
        # Command given wasn't valid
        case _:
            await ctx.send('Invalid command. Try !fun-facts, !fun-facts get *id*, !fun-facts add "insert fact here", or !fun-facts remove *id*.')

@bot.command(name = "gamba")
async def gambling(ctx, command = '', value = ''):
    command = command.lower()
    value = value.lower()
    guild_id = ctx.guild.id
    folder_path = 'gamble'
    file_path = (f'{folder_path}/{guild_id}gamble.json')

    match command:
        # Sets up the files for storing player info
        case 'setup':
            await gamble.initialize(ctx, file_path, folder_path)
        # Returns a list of players based on the server it's being called from
        case 'players':
            await gamble.get_players(ctx, file_path)
        case 'points':
            await gamble.get_points(ctx, file_path)
        case 'game':
            await gamble.play_game(ctx, file_path, value, bot)
        case _:
            await ctx.send('Invalid command. Try !gamba setup, !gamba players, !gamba points, or !gamba game')

@bot.command(name = "wow")
async def worldofwarcraft(ctx, command = '', value = ''):
    command = command.lower()
    folder_path = 'worldofwarcraft'

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    match command:
        # Print random fact
        case '':
            file_path = await __create_path(folder_path, command, 'wowspecs.json', value)

            await wow_stuff.random_class(file_path, ctx)
        case 'dps':
                file_path = await __create_path(folder_path, command, 'wowspecsdps.json', value)

                await wow_stuff.random_class(file_path, ctx)
        case 'healer':
            file_path = await __create_path(folder_path, command, 'wowspecshealers.json', value)

            await wow_stuff.random_class(file_path, ctx)
        case 'tank':
            file_path = await __create_path(folder_path, command, 'wowspecstanks.json', value)

            await wow_stuff.random_class(file_path, ctx)
        case _:
            await ctx.send('Invalid command. Try !wow, !wow dps, !wow tank, or !wow healer.')

async def __create_path(folder_path, command, file_name, value):
    if (value == "ranged" or value == "melee") and command == 'dps':
        file_path = (f'{folder_path}/{value}{file_name}')
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                data = { "classes": [] }
                json.dump(data, file, indent = 4)

    else:
        file_path = (f'{folder_path}/{file_name}')
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                data = { "classes": [] }
                json.dump(data, file, indent = 4)

    return file_path


bot.run(TOKEN)