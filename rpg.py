import os
from mysql.connector import connection

import discord
from discord.ext import commands

from rpg_game import intro

async def start_menu(ctx, bot, database):
  def check(msg):
    return msg.author == ctx.author and isinstance(msg.channel, discord.channel.DMChannel)
  
  cursor = database.cursor()
  id = ctx.author.id
  username = ctx.author.global_name

  query = 'SELECT * FROM users WHERE id = %s'
  user_id = (id, )
  cursor.execute(query, user_id)
  result = cursor.fetchall()
  
  if (result == []):
    await create_character(ctx, bot, database, username, id, cursor)

  else:
    await ctx.author.send("You already have a character created. Would you like to resume from your most recent checkpoint? Please enter 'yes' or 'no'.")

    valid_response = False
    while(valid_response == False):
      msg = await bot.wait_for("message", check=check)

      if msg.content.lower()[0] == 'y':
        valid_response = True
        await get_checkpoint(ctx, bot, database)
      elif msg.content.lower()[0] == 'n':
        valid_response
        await create_character(ctx, bot, database)
      else:
        await ctx.author.send("Please enter a valid command.")

async def info(ctx):
  await ctx.send('This is a text-based RPG.')

async def create_character(ctx, bot, database, username, id, cursor):
  def check(msg):
    return msg.author == ctx.author and isinstance(msg.channel, discord.channel.DMChannel)
  
  registered = False
    
  await ctx.author.send('It would appear this is your first time playing. Please enter the name you want to use for your character.')
  msg = await bot.wait_for("message", check=check)
  char_name = msg.content
  progress_flag = 'INTRO'
      
  while (registered == False):
    await ctx.author.send(f"You said your name was {char_name}. Is this correct? Please enter 'yes' or 'no'.")
    msg = await bot.wait_for("message", check=check)

    if msg.content.lower()[0] == 'y':
      query = 'INSERT INTO users (id, username, char_name, progress_flag) VALUES (%s, %s, %s, %s)'
      new_values = (id, username, char_name, progress_flag)
      cursor.execute(query, new_values)
      database.commit()

      await ctx.author.send(f"Welcome, {char_name}, to the world of Yavallach.")
      registered = True
      
    else:
      await ctx.author.send("It would seem I got your name wrong. Tell me it again, and speak more clearly this time.")
      msg = await bot.wait_for("message", check=check)

    await ctx.author.send("With introductions out of the way, let us begin:")
    await intro.intro_begin(ctx, bot, database)

async def get_checkpoint(ctx, bot, database):
  cursor = database.cursor()
  id = ctx.author.id
  user_id = (id, )

  query = 'SELECT progress_flag FROM users WHERE id = %s'
  cursor.execute(query, user_id)
  result = cursor.fetchone()

  match result[0]:
    case 'INTRO':
      await intro.intro_begin(ctx, bot, database)


