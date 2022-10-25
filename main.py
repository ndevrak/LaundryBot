import discord # Discord API
from discord.ext import commands
from laundrybothelper import *

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

LH = LaundryHandler(client)

@client.event
async def on_ready():
  # Resets TAKEN values
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='clothes spin 👕'))
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    await LH.LaundryMessageHandler(message)

  

# Run Bot
client.run("ODE4NTYwOTk0MjA0MDU3NjEw.YEZ2VQ.LHd5zNfwJ6GGY8_NW1zRx7AAjgA")