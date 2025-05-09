import json
from random import randrange

async def random_class(file_path, ctx):
  with open(file_path, 'r') as file:
      data = json.load(file)
      if (len(data['classes']) != 0):
          # Use a randomizer to grab a random WoW spec from the list
          randomizer = randrange(len(data['classes']))
          await ctx.send('Your spec is: ' + data['classes'][randomizer]['spec'])
      else:
          await ctx.send("There are no classes to be had. :(")