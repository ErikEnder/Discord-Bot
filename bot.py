# bot.py
import os
import json
from dotenv import load_dotenv

import gamble
import fun_fact
import wow_stuff
import magic_ball
import mute_roulette

import discord
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

mute_active = False


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Adds a specific reaction to every message I send, but no one else.
@bot.event
async def on_message(message):
    if (message.author.bot):
        return

    if message.author.id == int(MY_ID):
        await message.add_reaction(EMOTE)

    # Inside joke
    if message.content.lower() == 'how' or message.content.lower() == 'how?':
        reply_to = await message.channel.fetch_message(message.id)
        await reply_to.reply("Are you illiterate?")
    
    await bot.process_commands(message)

@bot.command(name = 'funfact', description = "Have the bot print out a fun fact for everyone to enjoy, or edit the list yourself!")
async def fun_facts(ctx, command = commands.parameter(description = "Available commands: none, 'get', 'add', or 'remove'.", default = ''), input = commands.parameter(description = "Add = quotes, Get = integers, Remove = integers", default = '')):
    command = command.lower()
    guild_id = ctx.guild.id

    folder_path = 'fun_facts'

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    # Ensures a file is created if it doesn't already exist
    file_path = await __create_path(folder_path, 'funfacts.json', "facts", guild_id)
    
    # Creates the file to help pseudo-randomize the fun facts
    pseudo_path = await __create_path(folder_path, 'pseudorandom.json', "facts", guild_id)

    match command:
        case '':
            await fun_fact.random_fact(file_path, ctx, pseudo_path)
        case 'get':
            await fun_fact.specific_fact(file_path, ctx, input, pseudo_path)
        case 'add':
            await fun_fact.add_fact(file_path, pseudo_path, ctx, input)
        case 'remove':
            await fun_fact.remove_fact(file_path, ctx, input)
        case _:
            await ctx.send('Invalid command. Try !funfacts, !funfacts get *id*, !funfacts add "insert fact here", or !funfacts remove *id*')

@bot.command(name = "gamba")
async def gambling(ctx, command = '', game_name = ''):
    command = command.lower()
    game_name = game_name.lower()
    guild_id = ctx.guild.id
    folder_path = 'gamble'
    file_path = (f'{folder_path}/{guild_id}gamble.json')

    match command:
        case 'setup':
            await gamble.initialize(ctx, file_path, folder_path)
        case 'players':
            await gamble.get_players(ctx, file_path)
        case 'points':
            await gamble.get_points(ctx, file_path)
        case 'game':
            await gamble.play_game(ctx, file_path, game_name, bot)
        case _:
            await ctx.send('Invalid command. Try !gamba setup, !gamba players, !gamba points, or !gamba game')

@bot.command(name = "wow")
async def worldofwarcraft(ctx, command = '', range = ''):
    command = command.lower()
    range = range.capitalize()

    folder_path = 'worldofwarcraft'
    file_path = (f'{folder_path}/wowspecs.json')
    await wow_stuff.check_if_exists(folder_path, file_path)

    match command:
        case '':
            await wow_stuff.random_class(file_path, ctx)
    
        case 'dps':
            if range == '' or range == 'Ranged' or range == 'Melee':
                await wow_stuff.random_role(file_path, ctx, 'DPS', range)
            else:
                await ctx.send("Invalid range value. Please enter an empty value, 'ranged', or 'melee'.")

        case 'healer':
            range = ''
            await wow_stuff.random_role(file_path, ctx, 'Healer', range)
            
        case 'tank':
            range = ''
            await wow_stuff.random_role(file_path, ctx, 'Tank', range)

        case 'count':
            await wow_stuff.class_count(file_path, ctx)
            
        case _:
            await ctx.send('Invalid command. Try !wow, !wow dps, !wow tank, or !wow healer')

@bot.command(name = '8ball')
async def magic_eight_ball(ctx, *, arg):
    folder_path = 'magicball'
    file_path = f'{folder_path}/magic_eight_ball.json'

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    await magic_ball.check_if_exists(folder_path, file_path)

    await magic_ball.random_response(file_path, ctx)

@bot.command(name = 'temp')
async def temperature_converter(ctx, command = '', temperature = ''):
    command = command.lower()
    if (command == 'f2c' or command == 'c2f'):
        if (temperature.isdigit()):
            match command:
                case 'f2c':
                    await ctx.send(f"{temperature} degrees Fahrenheit is equal to {await __temp_conversion_display(temperature, 'fahrenheit')} degrees Celsius.")
                case 'c2f':
                    await ctx.send(f"{temperature} degrees Celsius is equal to {await __temp_conversion_display(temperature, 'celsius')} degrees Fahrenheit.")
        else:
            await ctx.send("Improper value. Please enter a valid number.")
    else:
        await ctx.send("Improper command. Use '!temp f2c' for Fahrenheit to Celsius, or '!temp c2f' for Celsius to Fahrenheit.")

@bot.command(name = 'mute')
async def mute_roulette_activation(ctx, command = ''):
    command = command.lower()
    match command:
        case 'on':
            mute_active = True
            await mute_roulette.mute_roulette_logic(ctx, mute_active)
        case 'off':
            mute_active = False
            await mute_roulette.mute_roulette_logic(ctx, mute_active)
        case _:
            ('Invalid command. Try !mute on OR !mute off')

    
    


async def __temp_conversion_display(temperature, temperature_unit):
    temperature = float(temperature)

    # Fahrenheit to Celsius
    if (temperature_unit == 'fahrenheit'):
        conversion = round((temperature - 32) * (5/9), 1)
        decimal_digit = int((conversion * 10) % 10)

    # Celsius to Fahrenheit
    elif (temperature_unit == 'celsius'):
        conversion = round((temperature * (9/5)) + 32, 1)
        decimal_digit = int((conversion * 10) % 10)

    # If the decimal is 0, remove it from the output for a cleaner look
    if (decimal_digit == 0):
        return int(conversion)
    else:
        return conversion


# Used for creating files that do not need to be populated on creation
async def __create_path(folder_path, file_name, data_header: str, guild_id = ''):
    if guild_id == '':
        file_path = (f'{folder_path}/{file_name}')
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                data = { f"{data_header}": [] }
                json.dump(data, file, indent = 4)
    
    else:
        file_path = (f'{folder_path}/{guild_id}{file_name}')
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                data = { f"{data_header}": [] }
                json.dump(data, file, indent = 4)

    return file_path



bot.run(TOKEN)