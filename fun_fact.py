import os
import json
from random import randrange

async def random_fact(file_path, ctx, pseudo_path):
  with open(file_path, 'r') as file:
      data = json.load(file)
      if (len(data['facts']) != 0):
          # Use a randomizer to grab a random fact from the list
          randomizer = randrange(len(data['facts']))
          fact_id = data['facts'][randomizer]['id']
          await ctx.send('Fact #' + str(fact_id) + ': ' + data['facts'][randomizer]['fact'])
          await __pseudo_randomize(fact_id, file_path, pseudo_path)
      else:
          await ctx.send("There are no fun facts to be had. :(")

async def specific_fact(file_path, ctx, value, pseudo_path):
    valid_value_main = False
    valid_value_pseudo = False
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for i in data['facts']:
                if i['id'] == int(value):
                    valid_value_main = True
                    break
                else:
                    valid_value_main = False

        # If ID is not found in main file, check pseudo file to make sure it's not hidden there after random facts
        if (not valid_value_main):
            with open(pseudo_path, 'r') as pseudo:
                data = json.load(pseudo)
                for i in data['facts']:
                    if i['id'] == int(value):
                        valid_value_pseudo = True
                        break
                    else:
                        valid_value_pseudo = False

        # If ID is found in either main file or pseudo file, print it
        if (valid_value_main or valid_value_pseudo):
            await ctx.send(i['fact'])
        # If ID isn't found in either file, it doesn't exist
        else:
            await ctx.send(f'No facts with an ID of {value} exist.')
    except ValueError:
        await ctx.send("Please enter a valid ID.")

async def add_fact(file_path, pseudo_path, ctx, value):
     # Opening pseudo file first since we won't use it again but we need to capture its max_id
     with open(pseudo_path, 'r') as pseudo:
         pseudo_data = json.load(pseudo)
         if (len(pseudo_data['facts']) != 0):
            max_pseudo_id = max([i.get('id', 0) for i in pseudo_data['facts']])
         else:
            max_pseudo_id = 0

     with open(file_path, 'r+') as file:
        if (len(value) >= 8):
            data = json.load(file)

            # find max ID so that it can iterate when a new fact is added
            if (len(data['facts']) != 0):
                max_id = max([i.get('id', 0) for i in data['facts']])
            else:
                max_id = 0
            
            # Want to figure out if pseudo has a higher ID in it, and to iterate on that instead if possible.
            # This should avoid repeat IDs getting generated.
            if (max_pseudo_id > max_id):
                new_fact = {"id": (max_pseudo_id + 1),
                            "fact": value
                        }
            else:
                new_fact = {"id": (max_id + 1),
                            "fact": value
                        }
                    
            data['facts'].append(new_fact)
            file.seek(0)
            json.dump(data, file, indent = 4)
                    
            # Delete the message of the person who submitted the fact to keep it anonymous.
            await ctx.message.delete()
            await ctx.send(f'Your fact was added. Its ID is {new_fact['id']}.')
        # Ideally helps avoid bad data and/or typos
        elif ((len(value) < 8) & (value != '')):
            await ctx.send("What kind of fact is less than 8 characters? I'm not adding that.")
        else:
            await ctx.send("You didn't enter a fact. I won't add nothing, that's impossible!")

async def remove_fact(file_path, ctx, value):
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
            # If not done this way, the file tends to break. There's probably a workaround for it, but this is simpler.
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

async def __pseudo_randomize(fact_id: int, file_path: str, pseudo_path: str):
    # Use the ID to find the fact in the main file
    with open(file_path, 'r+') as main_file:
        data = json.load(main_file)
        data_length = len(data['facts'])

        for i in data['facts']:
            if i['id'] == fact_id:
                copied_fact = {"id": i['id'],
                               "fact": i['fact']
                            }
                data['facts'].remove(i)
                new_data = data
                break
        
    # Copy the data from the main file to the pseudo file
    with open(pseudo_path, 'r+') as pseudo:
        pseu_data = json.load(pseudo)
        restored_list = []

        pseu_data['facts'].append(copied_fact)

        pseu_data_length = len(pseu_data['facts'])
        check_number = pseu_data_length

        # Check the length of the pseudo file
        # If length of pseudo file is equal to or higher than 1/3 of total entries, re-add the earliest entry to main file
        if (check_number > ((data_length + pseu_data_length) // 3)):
            while (check_number > ((data_length + pseu_data_length) // 3)):
                restored_list.append(pseu_data['facts'].pop(0))
                check_number -= 1

    # Delete old file and create new one with same name using the modified data
    with open(pseudo_path, 'w') as pseudo_ow:
        json.dump(pseu_data, pseudo_ow, indent = 4)

    # When an entry is restored, add it back to the main file
    with open(file_path, 'w') as file:
        for fact in restored_list:
            new_data['facts'].append(fact)
        
        file.seek(0)
        json.dump(new_data, file, indent = 4)