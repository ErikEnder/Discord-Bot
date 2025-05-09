import os
import json
from dotenv import load_dotenv
import asyncio
import time
import threading
import random

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
                legal_name = await __legal_name(ctx)

                await ctx.send(f"{legal_name} currently has: {player['points']} points.")
                break

async def play_game(ctx, file_path, value, bot):
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower()[0] in ['y', 'n']
    
    legal_name = await __legal_name(ctx)
    
    match value:
        case 'death roll':
            await ctx.send(f"{legal_name} has chosen to play Death Roll.")
            time.sleep(1)
            await ctx.send("Would you like to see the rules? Type 'y' or 'n', with 'n' taking you straight to the game.")
            try:
                msg = await bot.wait_for("message", check=check, timeout=15)
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you didn't reply in time!")

            if msg.content.lower()[0] == 'y':
                time.sleep(1)
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
                    time.sleep(1)
                    await __death_roll(ctx, file_path, bot)
                else:
                    time.sleep(1)
                    await ctx.send("Sounds good. Exiting out of game selection.")
            else:
                time.sleep(1)
                await ctx.send("Oh ya, you betcha. Sounds good ta me.")
                time.sleep(1)
                await __death_roll(ctx, file_path, bot)
        
        case 'free roll':
            await ctx.send(f"{legal_name} has chosen to play Free Roll.")
            time.sleep(1)
            await ctx.send("Would you like to see the rules? Type 'y' or 'n', with 'n' taking you straight to the game.")

            try:
                msg = await bot.wait_for("message", check=check, timeout=15)
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you didn't reply in time!")

            if msg.content.lower()[0] == 'y':
                time.sleep(1)
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
                    time.sleep(1)
                    await __free_roll()
                else:
                    time.sleep(1)
                    await ctx.send("Sounds good. Exiting out of game selection.")
            else:
                time.sleep(1)
                await ctx.send("Oh ya, you betcha. Sounds good ta me.")
                time.sleep(1)
                await __free_roll()
                
        case _:
            await ctx.send("No games selected. Would you like to see what's available? Type 'y' or 'n'.")

            try:
                msg = await bot.wait_for("message", check=check, timeout=15)
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you didn't reply in time!")

            if msg.content.lower()[0] == 'y':
                await ctx.send("Currently available games are:" \
                "\n1. Death Roll: A high-stakes winner takes all game of 'dice' rolling." \
                "\n2. Free Roll: A lower-stakes game where only the lowest rolling player loses their points.")
            else:
                await ctx.send("Then I guess you'll never know.")

async def __death_roll(ctx, file_path, bot):
    with open(file_path, 'r') as file:
        data = json.load(file)
        for player in data['players']:
            if player['id'] == ctx.author.id:
                host = player
                print(host)
                break
    
    legal_name = await __legal_name(ctx)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower()[0] in ['y', 'n', 'q']
    
    def bet(msg):
        try:
            return (msg.author == ctx.author and msg.channel == ctx.channel and float(msg.content) < 0) or (msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isdigit())
        except ValueError:
            bot.loop.create_task(ctx.channel.send("That... that's not an integer, man. C'mon."))

    await ctx.send("Welcome to Death Roll, a high-stakes winner takes all game of 'dice' rolling.")

    bet_placed = False
    while (not bet_placed):
        time.sleep(1.5)
        await ctx.send(f"\n\n\n{legal_name}, please enter the amount you want to bet. This will be the price of entry for all participants. You may enter 0 to play a free game, or any integer higher than 0.")
        try:
            msg = await bot.wait_for("message", check=bet, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time!")
            return
    
        try:
            if int(msg.content) >= 0 and int(msg.content) <= host['points']:
                host_bet = int(msg.content)

                await ctx.send(f"You've placed a bet of {msg.content} points. Is this correct? Enter 'y' or 'n'. You may also quit the game with 'q'.")
                try:
                    msg = await bot.wait_for("message", check=check, timeout=30)
                except asyncio.TimeoutError:
                    await ctx.send("Sorry, you didn't reply in time!")
                    bet_placed = False
                    
                if msg.content.lower()[0] == 'y':
                    bet_placed = True
                elif msg.content.lower()[0] == 'n':
                    bet_placed = False
                else:
                    await ctx.send("Ok, maybe next time then...")
                    return
            elif int(msg.content) < 0:
                await ctx.send("I bet you thought you were really clever entering a negative number, didn't you? Well guess what? I'm stealing the absolute value of your stupid bet, so the joke's on you.")
                deduction = int(msg.content) * -1

                with open(file_path, 'r+') as file:
                    data = json.load(file)
                    for player in data['players']:
                        if player['id'] == host['id']:
                            player['points'] -= deduction
                            break
                        
                    file.seek(0)
                    json.dump(data, file, indent = 4)

                return
            else:
                await ctx.send("You can't go into debt here, I wouldn't want to have to break your legs. Try entering a bet you can actually pay.")
        except ValueError:
            await ctx.send("I'm not sure what you did to break this, but congrats I guess.")
    
    await ctx.send(f"{legal_name} has entered their bet of {host_bet}. Players may now join by typing 'bet {host_bet}'. You have 30 seconds. The host may also start the game early by typing 'start game'.")
    
    
    
    collected_rollers = []
    t = 30
    timer_thread = threading.Thread(target = __countdown, args = (t,ctx,bot,))
    timer_thread.start()

    def signup(msg):
        if timer_thread.is_alive():
            with open(file_path, 'r') as file:
                data = json.load(file)
                for i in data['players']:
                    if i['id'] == msg.author.id:
                        player = i
            
            return (msg.channel == ctx.channel and player['points'] >= host_bet and msg.content.casefold()) == (f"bet {host_bet}") or (msg.channel == ctx.channel and msg.author.id == host['id'] and msg.content.casefold()) == ("start game")
        else:
            return True

    time_left = True
    while time_left:
        if timer_thread.is_alive():
            msg = await bot.wait_for('message', check=signup)
            player_exists = any(player['id'] == msg.author.id for player in collected_rollers)

            if (msg.content.casefold() == (f'bet {host_bet}') and not player_exists):
                await ctx.send(f'{await __legal_name(msg)} has signed up!')
                collected_rollers.append({ "id": msg.author.id, "name": await __legal_name(msg), "roll": 0, "hasRolled": False })
            elif (msg.content.casefold() == (f'bet {host_bet}') and player_exists):
                await ctx.send(f'{await __legal_name(msg)} is already entered. Stop spamming. >:(')
            elif (msg.content.casefold() == "start game"):
                await ctx.send(f'{legal_name} has started the game. Rolls will begin shortly...')
                time_left = False
                break
            else:
                break
        else:
            time_left = False
    
    await ctx.send('The participants for this match of Death Roll are: ')
    for roller in collected_rollers:
        await ctx.send(f"{roller['name']} \n")
    
    time.sleep(1)
    await ctx.send("LET'S GET READY TO ROLL DOWN!")
    time.sleep(2)
    await __death_roll_game(ctx, bot, collected_rollers)

async def __death_roll_game(ctx, bot, collected_rollers):
    round = 1
    round_total = len(collected_rollers) - 1
    if round_total < 1:
        round_total = 1
    game_active = True

    await ctx.send("Welcome to Death Roll. In this round-based game mode, each player rolls between 1 and 100 and the person with the lowest roll loses, getting themselves eliminated from the rest of the match.")
    time.sleep(2.5)
    await ctx.send("This will continue until there is only one player left, in which case they'll be crowned the winner and take home the entire pot of points. Huge.")
    time.sleep(2.5)
    await ctx.send("If two or more players tie in a round, they roll again. This continues until someone rolls a lower number than their opponent, eliminating them immediately. Rolling a '69' automatically wins you the current round.")
    time.sleep(2.5)
    await ctx.send("Easy enough, right? Then let's get started.")
    time.sleep(2.5)

    # def roll(msg):
    #     player_exists = any(player['id'] == msg.author.id for player in collected_rollers)
    #     return (player_exists and msg.channel == ctx.channel and msg.content.casefold() == 'roll')

    while game_active:
        await ctx.send(f"Round {round} of {round_total}")
        collected_rollers = await __rolldown(collected_rollers, ctx, bot, round, round_total)

        
        time.sleep(2)
        await ctx.send("It looks like everyone is done rolling. You probably already know the results, but let's make it official, shall we?")

        results = await __compare_rolls(collected_rollers, ctx)
        print(results)
        tiebreaker = results[0]['tiebreaker']
        
        while (tiebreaker):
            await ctx.send(f"Well butter my biscuits, we've got ourselves a good ol' fashioned tiebreaker. Alright, pardners, let's get on wit' it.")
            tiebreaker_rollers = await __rolldown(set(results[0]['rollers']), ctx, bot, round, round_total)
            results = await __compare_rolls(tiebreaker_rollers, ctx)
            print(results)
            tiebreaker = results[0]['tiebreaker']

        time.sleep(2.5)
        await ctx.send(f"And just like that, {results[0]['loser_name']} is off to the guillotine. Better luck next time, bud. Why don't the rest of you pour one out for 'em?")
        for roller in collected_rollers:
            if roller['id'] == results[0]['loser_id']:
                collected_rollers.remove(roller)

        time.sleep(2.5)
        if (round == (round_total - 1)):
            await ctx.send("Final round coming up. Get ready.")
            round += 1
        elif (round >= round_total):
            await ctx.send("And that's a wrap.")
            time.sleep(1.5)
            await ctx.send(f"Congratulations to {results[0]['winner_name']} on winning the Death Roll! Enjoy your victory.")
            game_active = False
        else:
            await ctx.send("Alright, that's enough of that. Next round coming up...")
            round += 1
        time.sleep(2.5)





    
async def __free_roll():
    return

async def __legal_name(ctx):
    if (ctx.author.nick == None):
        return ctx.author.global_name
    else:
        return ctx.author.nick
    
async def __find_player(ctx, file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        for player in data['players']:
            if player['id'] == ctx.author.id:
                return player
            
def __countdown(t, ctx, bot):
        sleep_duration = t
        while sleep_duration > 0:
            print(f"you have {sleep_duration} seconds left")
            time.sleep(1)
            sleep_duration -= 1
        bot.loop.create_task(ctx.channel.send("Time's up."))
        time.sleep(1)

async def __rolldown(collected_rollers, ctx, bot, round, round_total):
    def roll(msg):
        player_exists = any(player['id'] == msg.author.id for player in collected_rollers)
        return (player_exists and msg.channel == ctx.channel and msg.content.casefold() == 'roll')
    
    for player in collected_rollers:
            player['hasRolled'] = False

    time.sleep(2.5)
    await ctx.send("Players may now roll by typing 'roll'. Remember, you only get one per round.")
    for _ in range (len(collected_rollers)):
        msg = await bot.wait_for('message', check=roll)
        random_roll = random.randint(1, 100)
        if (random_roll == 69):
            await ctx.send(f"{await __legal_name(msg).upper()} ROLLED {random_roll}! OH MY SWEET NUGGETS! I'VE ONLY HEARD LEGENDS BEFORE TODAY, BUT THEY'VE ACTUALLY DONE IT!")
        elif (random_roll == 100):
            await ctx.send(f"{await __legal_name(msg)} rolled {random_roll}! They're practically invincible!")
        elif (random_roll > 80):
            await ctx.send(f"{await __legal_name(msg)} rolled {random_roll}! Wow, that's gonna be hard to beat!")
        elif (random_roll > 60 and random_roll < 80 and random_roll != 69):
            await ctx.send(f"{await __legal_name(msg)} rolled {random_roll}! Not too shabby!")
        elif (random_roll > 40 and random_roll < 60):
            await ctx.send(f"{await __legal_name(msg)} rolled {random_roll}! Uh oh, they might be in hot water!")
        elif (random_roll > 20 and random_roll < 40):
            await ctx.send(f"{await __legal_name(msg)} rolled {random_roll}! Oh no...")
        else:
            await ctx.send(f"{await __legal_name(msg)} rolled {random_roll}! They're gonna need a miracle to survive this one! Pray to whatever gods you believe in.")

        for player in collected_rollers:
            if player['id'] == msg.author.id:
                player['roll'] = random_roll
                player['hasRolled'] = True
    
    return collected_rollers

async def __compare_rolls(collected_rollers, ctx):
    lowest_roll = 0
    lowest_id = 0
    loser_name = ''

    highest_roll = 0
    highest_id = 0
    winner_name = ''

    tiebreaker = False
    tiebreaker_rollers = []

    for player in collected_rollers:
        if player['roll'] < lowest_roll or lowest_roll == 0:
            lowest_roll = player['roll']
            lowest_id = player['id']
            loser_name = player['name']

            # Remove any tiebreaker rollers if a new lowest value is found
            for roller in tiebreaker_rollers:
                tiebreaker_rollers.remove(roller)
            
            # Add a new potential tiebreaker roller
            tiebreaker_rollers.append(player)

            tiebreaker = False

        elif player['roll'] > highest_roll or highest_roll == 0:
            highest_roll = player['roll']
            highest_id = player['id']
            winner_name = player['name']

        elif player['roll'] == lowest_roll:
            tiebreaker = True
            tiebreaker_rollers.append(player)
        else:
            pass


    if (tiebreaker):
        return [{ "rollers": tiebreaker_rollers, "tiebreaker": True}]
    else:
        return [{ "loser_id": lowest_id, "loser_name": loser_name, "winner_id": highest_id, "winner_name": winner_name, "tiebreaker": False }]