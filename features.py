import json

async def add_feature(file_path, ctx, request):
  with open(file_path, 'r+') as file:
      data = json.load(file)

      if (len(data['requests']) != 0):
          max_id = max([i.get('id', 0) for i in data['requests']])
      else:
          max_id = 0
            
    
      new_request = {"id": (max_id + 1),
                     "feature": request
                  }
                    
      data['requests'].append(new_request)
      file.seek(0)
      json.dump(data, file, indent = 4)

      await ctx.send(f'Request added.')

async def show_list(file_path, ctx):
    list_string = ''
    with open(file_path, 'r') as file:
        data = json.load(file)

        if (len(data['requests']) != 0):
            print('Current list: ' + list_string)
            for i in data['requests']:
                list_string += (f'{i['feature']} \n')
                print('Current list: ' + list_string)

    await ctx.send(f'''Current requests: \n{list_string} ''')