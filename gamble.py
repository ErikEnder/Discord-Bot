import os
import json
from dotenv import load_dotenv
import asyncio

import discord


load_dotenv()
SERVER_ID = os.getenv('SERVER_ID')
ROLE_ID = os.getenv('ROLE_ID')

async def initialize(ctx, file_path, folder_path):
    mem_list = []
    
    # Checks if the bot is being called from a specific server, and if it is then it uses a specific role to populate the list
    if ctx.guild.id == int(SERVER_ID):
      for member in ctx.guild.members:
        for role in member.roles:
          if role.id == int(ROLE_ID):
            mem_list.append({ "id": member.id, "name": member.global_name, "nickname": member.nick, "points": 10000 })
    # Otherwise populate the list with all server members
    else:
        for member in ctx.guild.members:
            mem_list.append({ "id": member.id, "name": member.global_name, "nickname": member.nick, "points": 10000 })

    # Creates a directory if it doesn't already exist
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    # Ensures a file is created if it doesn't already exist
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            data = { "players": mem_list }
            json.dump(data, file, indent = 4)
            await ctx.send('First time setup complete.')
    else:
        mem_ids = []
        for member in mem_list:
            mem_ids.append(member['id'])

        with open(file_path, 'r+') as file:
            data = json.load(file)
            existing_players = []
            for player in data['players']:
                existing_players.append(player['id'])
            
            # Compares all (valid) users of a server to the already existing players in a list 
            # and returns the IDs of any players who haven't already been added to the list
            new_players_ids = list(set(mem_ids) - set(existing_players))
            
            # If there are new players, compare their IDs to the list of server members
            # This is done to get their full server information for list population purposes
            if len(new_players_ids) > 0:
                for member in mem_list:
                  for player in new_players_ids:
                      if int(member['id']) == player:
                          new_player = {"id": int(member['id']),
                                    "name": member['name'],
                                    "points": 10000
                                  }
                          data['players'].append(new_player)
                file.seek(0)
                json.dump(data, file, indent = 4)
                await ctx.send('New players added.')
            else:
                await ctx.send('All players already accounted for.')

async def get_players(ctx, file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    await ctx.send("\n\nName: ".join(str(player['name']) + '\nPoints: ' + str(player['points']) for player in data['players']))

async def get_points(ctx, file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

        for player in data['players']:
            if int(player['id']) == ctx.author.id:
                await ctx.send(f"{ctx.author.nick} currently has: {player['points']} points.")
                break

async def play_game(ctx, file_path, value, bot):
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower()[0] in ['y', 'n']
    
    match value:
        case 'death roll':
            await ctx.send(f"{ctx.author.nick} has chosen to play Death Roll.")
            await ctx.send("Would you like to see the rules? Type 'y' or 'n', with 'n' taking you straight to the game.")
            try:
                msg = await bot.wait_for("message", check=check, timeout=10)
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you didn't reply in time!")

            if msg.content.lower()[0] == 'y':
                await ctx.send("Rules for Death Roll:" \
                "\nRule 1: The player who initiated the Death Roll selects a bet amount. All players must match that bet to play." \
                "\nRule 2: All players will roll from 1 - 100. Anyone who doesn't roll before the timer expires will be disqualified and lose their bet." \
                "\nRule 3: Once the rolls have been tallied, the player with the lowest roll will be disqualified and lose their bet." \
                "\nRule 4: The game continues with the remaining players until only one is left, at which point they will be declared the winner and take the entire pot.")

                await ctx.send("\n\nContinue to the game? Type 'y' or 'n'.")
                try:
                    msg = await bot.wait_for("message", check=check, timeout=30)
                except asyncio.TimeoutError:
                    await ctx.send("I'll take that as a no. Exiting out of game selection.")
                
                if msg.content.lower()[0] == 'y':
                    await __death_roll()
                else:
                    await ctx.send("Sounds good. Exiting out of game selection.")
            else:
                await ctx.send("Oh ya, you betcha. Sounds good ta me.")
                await __death_roll()
        
        case 'free roll':
            await ctx.send(f"{ctx.author.nick} has chosen to play Free Roll.")
            await ctx.send("Would you like to see the rules? Type 'y' or 'n', with 'n' taking you straight to the game.")

            try:
                msg = await bot.wait_for("message", check=check, timeout=10)
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you didn't reply in time!")

            if msg.content.lower()[0] == 'y':
                await ctx.send("Rules for Free Roll:" \
                "\nRule 1: The player who initiated the Free Roll selects a bet amount. All players must match that bet to play." \
                "\nRule 2: All players will roll from 1 - 100. The winner is the player with the highest roll, and the loser is the player with the lowest roll." \
                "\nRule 3: Only the player with the lowest roll will lose their points, and only the player with the highest roll will earn them.")

                await ctx.send("\n\nContinue to the game? Type 'y' or 'n'.")
                try:
                    msg = await bot.wait_for("message", check=check, timeout=30)
                except asyncio.TimeoutError:
                    await ctx.send("I'll take that as a no. Exiting out of game selection.")
                
                if msg.content.lower()[0] == 'y':
                    await __free_roll()
                else:
                    await ctx.send("Sounds good. Exiting out of game selection.")
            else:
                await ctx.send("Oh ya, you betcha. Sounds good ta me.")
                await __free_roll()
                
        case _:
            await ctx.send("No games selected. Would you like to see what's available? Type 'y' or 'n'.")

            try:
                msg = await bot.wait_for("message", check=check, timeout=10)
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you didn't reply in time!")

            if msg.content.lower()[0] == 'y':
                await ctx.send("Currently available games are:" \
                "\n1. Death Roll: A high-stakes winner takes all game of 'dice' rolling." \
                "\n2. Free Roll: A lower-stakes game where only the lowest rolling player loses their points.")
            else:
                await ctx.send("Then I guess you'll never know.")

async def __death_roll():
    return

async def __free_roll():
    return