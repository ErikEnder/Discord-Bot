import time

from random import randrange

async def mute_roulette_logic(ctx, mute_state: bool):
  voice_list = ([])
  target_muted = False

  while (mute_state):
    print("Starting loop")
    update_countdown = 5
    for x in range(update_countdown):
        time.sleep(1)

    for member in ctx.guild.members:
            voice_state = member.voice
            if voice_state is None:
                continue
            else:
                voice_list.append(member.id)

    while (target_muted != True):
      randomizer = randrange(len(voice_list))

      target_member = ctx.guild.get_member(voice_list[randomizer])
      print(target_member)

      
      # Just in case person leaves voice in between the list being created and them being targeted
      if target_member.voice != None:
          await target_member.edit(mute = True)
          target_muted = True
      else:
          voice_list.remove(target_member.id)

    
    while(target_member.voice.mute == True):
        unmute_countdown = randrange(10)
        await ctx.send(f"User {target_member.name} has been muted for {unmute_countdown} seconds. Unlucky.")

        for x in range(unmute_countdown):
            time.sleep(1)
        
        await target_member.edit(mute = False)
        target_muted = False
        await ctx.send(f"User {target_member.name} is now unmuted. Free at last.")
    


    # If mute is active then:
    # Have a timer that, when it hits 0, randomly mutes someone currently in a voice chat

    # 1. Timer/Loop
    # 2. Upon reaching 0 in timer, check server roster
    # 3. Check if anyone from current channel roster is in a voice chat
    # 4. Put all members currently in a voice chat into a list
    # 5. Use a randomizer to pick someone from the list and mute them
    # 6. Store the person who was muted so that after an amount of time they are unmuted
    # 7. Repeat. Ensure the mute timer does not run until there is no one muted.
