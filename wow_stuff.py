import json
import os

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

async def random_role(file_path, ctx, role, range):
    spec_list = []
    with open(file_path, 'r') as file:
        data = json.load(file)
        if (len(data['classes']) != 0):
            for i in data['classes']:
                if i['role'] == role:
                    # If range isn't an empty string, then it should be "ranged" or "melee". If so, make sure the specs being added match that modifier.
                    if range != '':
                        if i['range'] == range:
                            # If the role matches the query, add the name of the spec to the list
                            spec_list.append(i['spec'])
                    # If range is an empty string, then just add specs that match the role
                    else:
                        spec_list.append(i['spec'])
    
    if len(spec_list) != 0:
        randomizer = randrange(len(spec_list))
        await ctx.send('Your spec is: ' + spec_list[randomizer])


# Automatically creates and populates the list with currently available classes in WoW as of 5/22/2025
async def check_if_exists(folder_path, file_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            data = { "classes": [
                            { "id": 1,
                            "spec": "Blood Death Knight",
                            "role": "Tank",
                            "range": "Melee"
                            },
                            { "id": 2,
                            "spec": "Frost Death Knight",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 3,
                            "spec": "Unholy Death Knight",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 4,
                            "spec": "Havoc Demon Hunter",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 5,
                            "spec": "Vengeance Demon Hunter",
                            "role": "Tank",
                            "range": "Melee"
                            },
                            { "id": 6,
                            "spec": "Balance Druid",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 7,
                            "spec": "Feral Druid",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 8,
                            "spec": "Guardian Druid",
                            "role": "Tank",
                            "range": "Melee"
                            },
                            { "id": 9,
                            "spec": "Restoration Druid",
                            "role": "Healer",
                            "range": "Ranged"
                            },
                            { "id": 10,
                            "spec": "Augmentation Evoker",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 11,
                            "spec": "Devastation Evoker",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 12,
                            "spec": "Preservation Evoker",
                            "role": "Healer",
                            "range": "Ranged"
                            },
                            { "id": 13,
                            "spec": "Beast Mastery Hunter",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 14,
                            "spec": "Marksmanship Hunter",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 15,
                            "spec": "Survival Hunter",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 16,
                            "spec": "Arcane Mage",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 17,
                            "spec": "Fire Mage",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 18,
                            "spec": "Frost Mage",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 19,
                            "spec": "Brewmaster Monk",
                            "role": "Tank",
                            "range": "Melee"
                            },
                            { "id": 20,
                            "spec": "Mistweaver Monk",
                            "role": "Healer",
                            "range": "Melee"
                            },
                            { "id": 21,
                            "spec": "Windwalker Monk",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 22,
                            "spec": "Holy Paladin",
                            "role": "Healer",
                            "range": "Melee"
                            },
                            { "id": 23,
                            "spec": "Protection Paladin",
                            "role": "Tank",
                            "range": "Melee"
                            },
                            { "id": 24,
                            "spec": "Retribution Paladin",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 25,
                            "spec": "Discipline Priest",
                            "role": "Healer",
                            "range": "Ranged"
                            },
                            { "id": 26,
                            "spec": "Holy Priest",
                            "role": "Healer",
                            "range": "Ranged"
                            },
                            { "id": 27,
                            "spec": "Shadow Priest",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 28,
                            "spec": "Assassination Rogue",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 29,
                            "spec": "Outlaw Rogue",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 30,
                            "spec": "Subtlety Rogue",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 31,
                            "spec": "Elemental Shaman",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 32,
                            "spec": "Enhancement Shaman",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 33,
                            "spec": "Restoration Shaman",
                            "role": "Healer",
                            "range": "Ranged"
                            },
                            { "id": 34,
                            "spec": "Affliction Warlock",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 35,
                            "spec": "Demonology Warlock",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 36,
                            "spec": "Destruction Warlock",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 37,
                            "spec": "Arms Warrior",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 38,
                            "spec": "Fury Warrior",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 39,
                            "spec": "Protection Warrior",
                            "role": "Tank",
                            "range": "Melee"
                            }
                        ]
                    }
            json.dump(data, file, indent = 4)    