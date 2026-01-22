import os
from mysql.connector import connection

import discord
from discord.ext import commands

async def intro_begin(ctx, bot, database):
  def check(msg):
    return msg.author == ctx.author and isinstance(msg.channel, discord.channel.DMChannel)
  
  await ctx.author.send("You awaken on a cold, stone floor and find yourself laying in what appears to be a prison cell made of gray stone. " \
  "There's a small, barred window that you wouldn't be able to fit through. Opposite it are larger bars that block access to a hallway, as well as a solid metal door.")
  await ctx.author.send("What do you want to do? \n\nHINT: Try typing 'explore cell' or 'check door' to potentially unveil details or secrets necessary to your success. 'Explore' commands are used to scout an area, while 'Check' commands are used to interact with potentially suspicious objects.\n\n" \
  "ACTION:")

  trapped_in_cell = True
  while (trapped_in_cell):
    msg = await bot.wait_for("message", check=check)
    await intro_cell_inputs(ctx, msg)

  
async def intro_cell_inputs(ctx, msg):
  msg = msg.content.lower()
  match msg:
      case 'explore cell':
        await ctx.author.send("You decide to explore the cell. The walls are unnaturally smooth, clearly man made through some means unknown to you. The floor consists of evenly sized slate gray tiles that measure roughly 1x1 feet in size.\n\n" \
        "As you're exploring you notice one of the tiles appears damaged and chipped on one of its sides, though everything else appears to be in perfect condition. \n\n" \
        "ACTION:")

      case 'check door':
        await ctx.author.send("You decide to check the metal door. At first glance it appears to be in impeccable condition. The metal is smooth and solid with a small open slot at the bottom, presumably for passing in supplies to inmates such as yourself. You test the door by pushing on it and feel it wiggle slightly upon the hinges.\n\n" \
        "You extend an arm through the bars and feel around until you find the handle. You attempt to turn it, but it doesn't give.\n\n" \
        "ACTION:")

      case 'check tile':
        await ctx.author.send("You go to examine the damaged tile more closely. You tap on it, but nothing happens. However, as you slide a finger into the chipped section, you feel the tile move slightly. You carefully manage to lift the tile up, revealing a hole in the ground.\n\n" \
        "Once removed, you find you can move several other tiles as well. For your efforts, you're rewarded with an interesting discovery: a burlap sack hidden beneath the floor of the prison cell.\n\n" \
        "ACTION:")

      case 'check sack':
        await ctx.author.send("You grab the sack and pull it up out of the hole in the ground. It's decently heavy, but you manage to lay it out onto the floor. The neck is tied with a rope, but with some effort you manage to undo the knot.\n\n" \
        "You open the sack and explore its contents to find something strange: inside there are an assortment of weapons, though you're not sure how they all fit inside. Pulling them out one-by-one reveals a large claymore sword that would likely require two hands to wield, a book with a mysterious inscribing on the cover, and a pair of twin daggers.\n\n" \
        "These weapons will certainly prove useful, but you realize you'd likely only be able to carry one of them. Which do you think you'd prefer? \n\nHINT: Try typing 'take sword', 'take book', or 'take daggers'. 'Take' commands are used to store items in your inventory, when possible.\n\n" \
        "ACTION:")
