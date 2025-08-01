import json
import os

from random import randrange

async def random_class(file_path, ctx):
  with open(file_path, 'r') as file:
      data = json.load(file)
      if (len(data['classes']) != 0):
          # Use a randomizer to grab a random WoW spec from the list
          randomizer = randrange(len(data['classes']))
          await ctx.send('Your spec is: ' + data['classes'][randomizer]['spec'] + ' ' + data['classes'][randomizer]['class'])
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
                            spec_list.append(i['spec'] + ' ' + i['class'])
                    # If range is an empty string, then just add specs that match the role
                    else:
                        spec_list.append(i['spec'] + ' ' + i['class'])
    
    if len(spec_list) != 0:
        randomizer = randrange(len(spec_list))
        await ctx.send('Your spec is: ' + spec_list[randomizer])

async def class_count(file_path, ctx):
    class_list = []
    tank_list = []
    ranged_dps_list = []
    melee_dps_list = []
    unknown_dps_list = [] # Kind of an error handler for bad data. They should all have ranges, but just in they don't they'll end up here.
    healer_list = []

    with open(file_path, 'r') as file:
        data = json.load(file)
        if (len(data['classes']) != 0):
            for i in data['classes']:
                role = i['role'].lower()
                wow_class = i['class']
                spec = i['spec']
                range = i['range'].lower()

                if (wow_class in class_list):
                    class_list = class_list
                else:
                    class_list.append(wow_class)

                match role:
                    case 'tank':
                        tank_list.append(spec + ' ' + wow_class)

                    case 'dps':
                        if (range == 'ranged'):
                            ranged_dps_list.append(spec + ' ' + wow_class)
                        elif (range == 'melee'):
                            melee_dps_list.append(spec + ' ' + wow_class)
                        else:
                            unknown_dps_list.append(spec + ' ' + wow_class)

                    case 'healer':
                        healer_list.append(spec + ' ' + wow_class)

    class_count = len(class_list)
    tank_count = len(tank_list)
    ranged_dps_count = len(ranged_dps_list)
    melee_dps_count = len(melee_dps_list)
    unknown_dps_count = len(unknown_dps_list)
    healer_count = len(healer_list)

    await ctx.send(f''' There are currently {tank_count + ranged_dps_count + melee_dps_count + unknown_dps_count + healer_count} specs in World of Warcraft between {class_count} classes. \nAmong those, there are {tank_count} tanks and {healer_count} healers. \nFor DPS specs there are a total of {ranged_dps_count + melee_dps_count}, with {ranged_dps_count} of those being ranged and the other {melee_dps_count} being melee.''')


# Automatically creates and populates the list with currently available classes in WoW as of 5/22/2025
async def check_if_exists(folder_path, file_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            data = { "classes": [
                            { "id": 1,
                            "class": "Death Knight",
                            "spec": "Blood",
                            "role": "Tank",
                            "range": "Melee"
                            },
                            { "id": 2,
                            "class": "Death Knight",
                            "spec": "Frost",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 3,
                            "class": "Death Knight",
                            "spec": "Unholy",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 4,
                            "class": "Demon Hunter",
                            "spec": "Havoc",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 5,
                            "class": "Demon Hunter",
                            "spec": "Vengeance",
                            "role": "Tank",
                            "range": "Melee"
                            },
                            { "id": 6,
                            "class": "Druid",
                            "spec": "Balance",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 7,
                            "class": "Druid",
                            "spec": "Feral",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 8,
                             "class": "Druid",
                            "spec": "Guardian",
                            "role": "Tank",
                            "range": "Melee"
                            },
                            { "id": 9,
                             "class": "Druid",
                            "spec": "Restoration",
                            "role": "Healer",
                            "range": "Ranged"
                            },
                            { "id": 10,
                            "class": "Evoker",
                            "spec": "Augmentation",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 11,
                            "class": "Evoker",
                            "spec": "Devastation",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 12,
                            "class": "Evoker",
                            "spec": "Preservation",
                            "role": "Healer",
                            "range": "Ranged"
                            },
                            { "id": 13,
                            "class": "Hunter",
                            "spec": "Beast Mastery",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 14,
                            "class": "Hunter",
                            "spec": "Marksmanship",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 15,
                            "class": "Hunter",
                            "spec": "Survival",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 16,
                            "class": "Mage",
                            "spec": "Arcane",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 17,
                            "class": "Mage",
                            "spec": "Fire",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 18,
                            "class": "Mage",
                            "spec": "Frost",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 19,
                            "class": "Monk",
                            "spec": "Brewmaster",
                            "role": "Tank",
                            "range": "Melee"
                            },
                            { "id": 20,
                            "class": "Monk",
                            "spec": "Mistweaver",
                            "role": "Healer",
                            "range": "Melee"
                            },
                            { "id": 21,
                            "class": "Monk",
                            "spec": "Windwalker",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 22,
                            "class": "Paladin",
                            "spec": "Holy",
                            "role": "Healer",
                            "range": "Melee"
                            },
                            { "id": 23,
                            "class": "Paladin",
                            "spec": "Protection",
                            "role": "Tank",
                            "range": "Melee"
                            },
                            { "id": 24,
                            "class": "Paladin",
                            "spec": "Retribution",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 25,
                            "class": "Priest",
                            "spec": "Discipline",
                            "role": "Healer",
                            "range": "Ranged"
                            },
                            { "id": 26,
                            "class": "Priest",
                            "spec": "Holy",
                            "role": "Healer",
                            "range": "Ranged"
                            },
                            { "id": 27,
                            "class": "Priest",
                            "spec": "Shadow",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 28,
                            "class": "Rogue",
                            "spec": "Assassination",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 29,
                            "class": "Rogue",
                            "spec": "Outlaw",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 30,
                            "class": "Rogue",
                            "spec": "Subtlety",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 31,
                            "class": "Shaman",
                            "spec": "Elemental",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 32,
                            "class": "Shaman",
                            "spec": "Enhancement",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 33,
                            "class": "Shaman",
                            "spec": "Restoration",
                            "role": "Healer",
                            "range": "Ranged"
                            },
                            { "id": 34,
                            "class": "Warlock",
                            "spec": "Affliction",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 35,
                            "class": "Warlock",
                            "spec": "Demonology",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 36,
                            "class": "Warlock",
                            "spec": "Destruction",
                            "role": "DPS",
                            "range": "Ranged"
                            },
                            { "id": 37,
                            "class": "Warrior",
                            "spec": "Arms",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 38,
                            "class": "Warrior",
                            "spec": "Fury",
                            "role": "DPS",
                            "range": "Melee"
                            },
                            { "id": 39,
                            "class": "Warrior",
                            "spec": "Protection",
                            "role": "Tank",
                            "range": "Melee"
                            }
                        ]
                    }
            json.dump(data, file, indent = 4)    