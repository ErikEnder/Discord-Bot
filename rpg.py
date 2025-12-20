import os
from mysql.connector import connection

import discord
from discord.ext import commands

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
        print(new_values)
        cursor.execute(query, new_values)
        database.commit()

        await ctx.author.send(f"Welcome, {char_name}, to the world of Yavallach.")
        registered = True
      
      else:
        await ctx.author.send("It would seem I got your name wrong. Tell me it again, and speak clearer this time.")
        msg = await bot.wait_for("message", check=check)

  await ctx.author.send("With introductions out of the way, let us begin:")

async def info(ctx):
  await ctx.send('This is a text-based RPG.')