import json
from random import randrange

async def random_response(file_path, ctx):
  with open(file_path, 'r') as file:
      data = json.load(file)
      if (len(data['answers']) != 0):
          # Use a randomizer to grab a random response from the list
          randomizer = randrange(len(data['answers']))
          await ctx.send(data['answers'][randomizer]['answer'])
      else:
          await ctx.send("I have no answers, for I am just a computer pretending to be a ball. :(")
