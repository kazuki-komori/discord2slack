import json
import os
from datetime import datetime, timedelta

import discord
import requests

TOKEN = os.getenv("BOT_TOKEN")
SLACK_URL = os.getenv("SLACK_URL")

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_voice_state_update(member, before, after):
  if before.channel == after.channel:
    pass
  else:
    now = datetime.utcnow() + timedelta(hours=9)
    if before.channel is None:
      msg = f":small_blue_diamond: {now:%m/%d-%H:%M}\n {after.channel} チャンネルに {member.name} が参加しました。\n {create_member_string(after)}\n"
    elif after.channel is None:
      msg = f":small_red_triangle_down: {now:%m/%d-%H:%M}\n {before.channel} チャンネルから {member.name} が退出しました。\n {create_member_string(after)}\n"
    else:
      msg = f":small_orange_diamond: {now:%m/%d-%H:%M}\n {member.name} が {before.channel} チャンネルから {after.channel} チャンネルに移動しました。\n {create_member_string(after)}\n"
    send_to_slack(msg)

def create_member_string(after):
  members = []
  if after.channel is not None:
      for member in after.channel.members:
        members.append(member.name)
      if len(members) == 1:
        return f":satellite: 参加者は {', '.join(members)} だけです。誰か入ってあげて!!"
      return f":satellite: 現在の参加者は {', '.join(members)} です。賑わってますね!"
  else:
    return f":satellite: 現在の参加者はいません :busts_in_silhouette:"

def send_to_slack(msg):
    payload = {
        "text": msg
    }
    headers = {'content-type': 'application/json'}
    response = requests.post(SLACK_URL, data=json.dumps(payload), headers=headers)
    print(response)

client.run(TOKEN)
