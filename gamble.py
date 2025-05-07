import os
import json
from dotenv import load_dotenv

import discord


load_dotenv()
SERVER_ID = os.getenv('SERVER_ID')
ROLE_ID = os.getenv('ROLE_ID')

async def initialize(ctx):
    guild_id = ctx.guild.id
    # Ensures the file being opened is relative to the server it's being called from
    file_path = (f'{guild_id}gamble.json')

    mem_list = []
    
    if ctx.guild.id == int(SERVER_ID):
      for member in ctx.guild.members:
        for role in member.roles:
          if role.id == int(ROLE_ID):
            mem_list.append({ "id": member.id, "name": member.global_name, "nickname": member.nick, "points": 10000 })
    else:
        for member in ctx.guild.members:
            mem_list.append({ "id": member.id, "name": member.global_name, "nickname": member.nick, "points": 10000 })

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
            
            new_players_ids = list(set(mem_ids) - set(existing_players))
            
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

async def get_players(ctx):
    guild_id = ctx.guild.id
    # Ensures the file being opened is relative to the server it's being called from
    file_path = (f'{guild_id}gamble.json')

    with open(file_path, 'r') as file:
        data = json.load(file)
    
    await ctx.send("\n\nName: ".join(str(player['name']) + '\nPoints: ' + str(player['points']) for player in data['players']))
            