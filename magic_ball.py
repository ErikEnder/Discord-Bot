import json
import os

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

async def check_if_exists(folder_path, file_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            data = { "answers": [
                    {
                    "id": 1,
                    "answer": "It is certain"
                    },
                    {
                    "id": 2,
                    "answer": "It is decidedly so"
                    },
                    {
                    "id": 3,
                    "answer": "Without a doubt"
                    },
                    {
                    "id": 4,
                    "answer": "Yes, definitely"
                    },
                    {
                    "id": 5,
                    "answer": "As I see it, yes"
                    },
                    {
                    "id": 6,
                    "answer": "Most likely"
                    },
                    {
                    "id": 7,
                    "answer": "Outlook good"
                    },
                    {
                    "id": 8,
                    "answer": "Signs point to yes"
                    },
                    {
                    "id": 9,
                    "answer": "Reply hazy, try again"
                    },
                    {
                    "id": 10,
                    "answer": "Ask again later"
                    },
                    {
                    "id": 11,
                    "answer": "Better not tell you now"
                    },
                    {
                    "id": 12,
                    "answer": "Cannot predict now"
                    },
                    {
                    "id": 13,
                    "answer": "Concentrate and ask again"
                    },
                    {
                    "id": 14,
                    "answer": "Don't count on it"
                    },
                    {
                    "id": 15,
                    "answer": "My sources say no"
                    },
                    {
                    "id": 16,
                    "answer": "Outlook not so good"
                    },
                    {
                    "id": 17,
                    "answer": "Very doubtful"
                    }
                ]}
            
            json.dump(data, file, indent = 4)    
