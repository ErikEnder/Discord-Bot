# bot.py
import os
import json
from random import randrange

import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
MY_ID = os.getenv('USER_ID')
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
    if message.author.id == int(MY_ID):
        await message.add_reaction(EMOTE)
    
    await bot.process_commands(message)

@bot.command(name = 'fun-facts', description = "Have the bot print out a fun fact for everyone to enjoy, or edit the list yourself!")
async def fun_facts(ctx, command = commands.parameter(description = "Available commands: none, 'add', or 'remove'.", default = ''), value = commands.parameter(description = "Add = quotes, Remove = integers", default = '')):
    command = command.lower()
    guild_id = ctx.guild.id

    # Ensures the file being opened is relative to the server it's being called from
    file_path = (f'{guild_id}funfacts.json') 

    # Ensures a file is created if it doesn't already exist
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            data = { "facts": [] }
            json.dump(data, file, indent = 4)

    match command:
        case '':
            with open(file_path, 'r') as file:
                data = json.load(file)
                if (len(data['facts']) != 0):
                    # Use a randomizer to grab a random fact from the list
                    randomizer = randrange(len(data['facts']))
                    await ctx.send('Fact #' + str(data['facts'][randomizer]['id']) + ': ' + data['facts'][randomizer]['fact'])
                else:
                    await ctx.send("There are no fun facts to be had. :(")
               
        case 'add':
            with open(file_path, 'r+') as file:
                if (len(value) >= 8):
                    data = json.load(file)

                    # find max ID so that it can iterate when a new fact is added
                    max_id = max([i.get('id', 0) for i in data['facts']])
                    new_fact = {"id": (max_id + 1),
                                "fact": value
                                }
                    
                    data['facts'].append(new_fact)
                    file.seek(0)
                    json.dump(data, file, indent = 4)
                    
                    # Delete the message of the person who submitted the fact to keep it anonymous.
                    await ctx.message.delete()
                    await ctx.send(f'Your fact was added. Its ID is {max_id + 1}.')
                # Ideally helps avoid bad data and/or typos
                elif ((len(value) < 8) & (value != '')):
                    await ctx.send("What kind of fact is less than 8 characters? I'm not adding that.")
                else:
                    await ctx.send("You didn't enter a fact. I won't add nothing, that's impossible!")
        case 'remove':
            valid_value = False

            try:
                # Open file to get current data and remove entry
                with open(file_path, 'r+') as file:
                    data = json.load(file)

                    for i in data['facts']:
                        if i['id'] == int(value):
                            data['facts'].remove(i)
                            new_data = data
                            valid_value = True
                            # Use break to stop the loop since there should only be one entry
                            break
                        else:
                            valid_value = False
                            
                if (valid_value):
                    # Delete old file and create new one with same name using the modified data
                    with open(file_path, 'w') as file:
                        json.dump(new_data, file, indent = 4)
                    
                    # Delete the message of the person who removed the fact to keep it anonymous.
                    await ctx.message.delete()
                    await ctx.send(f'Fact #{value} successfully removed.')

                else:
                    await ctx.send(f'No fact with an ID of {value} exists.')

            # Handles non-integer values being input
            except ValueError:
                    await ctx.send("Please enter a valid ID.")
        case _:
            await ctx.send('Invalid command.')

bot.run(TOKEN)