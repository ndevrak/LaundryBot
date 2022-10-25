import discord # Discord API
import os # --
from keep_alive import keep_alive # Keep Alive ping
import asyncio # Allows delayed functions without freezing
import ast # Allows interpreting .txt files as data type
import traceback # Provides error information
from replit import db

intents = discord.Intents.default()
intents.members = True
client = discord.Client()

# Washer / Dryer cycle times in minutes
W_TIME = 29
D_TIME = 45
# Channel ID for #laundry on Chi Psi Server
CHANNEL_ID = 823721207366680657
# Bot admins: Evan
# -- To get ID for user, type \@USER into Dicord chat
# -- Admin grants access to: .reset, .sendasbot
ADMINS = ['<@297502550037626891>','<@194640488043773952>',
'<@247226621377904641>']


@client.event
async def on_ready():
  # Resets TAKEN values
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='clothes spin 👕'))
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_error(event, *args, **kwargs):
  # Gets the message object and parses
  message = args[0]
  msgCausingError = message.content
  parsedMsgInfo = str(message).replace('>>','\n\n').replace('>','\n\n').replace('<','\n')
  # Gets error message from shell
  error = traceback.format_exc()
  # Sends message to #bot-error on Bot Test Server
  await client.get_channel(821506116134633494).send(
    '**EXCEPTION RAISED** '+ADMINS[0]+'\n\n`Message: '+msgCausingError+'`'+parsedMsgInfo+'`'+error+'`'
  )
  if ('X-RateLimit-Limit' in parsedMsgInfo):
    await client.get_channel(821506116134633494).send(
      '**RATE LIMIT REACHED** '+ADMINS[0]
    )
  print('--- EXCEPTION RAISED\n--- sent to Bot Test Server')
  print('Event: '+str(event))
  for item in args:
    print('args['+str(args.index(item))+']: '+str(item)+'\n')
  print('Error: '+error)
  return

@client.event
async def on_message(message):
  # Ignores messages sent by itself
  if message.author == client.user:
    return

  # Creates string that @'s message sender'
  atAuthor = '<@'+str(message.author.id)+'>'

  # initialize database
  if (message.content.startswith('.createdb')):
    db['W1_TAKEN']=False
    db['W2_TAKEN']=False
    db['D1_TAKEN']=False
    db['D2_TAKEN']=False
    db['W1_LAST']='Nikhil'
    db['W2_LAST']='Nikhil'
    db['D1_LAST']='Nikhil'
    db['D2_LAST']='Nikhil'
    return
  
  # .help laundry ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  if (message.content.startswith('.help laundry')):
    await message.channel.send(
      atAuthor+'\n__**Commands:**__\n`.washer1/.w1/.washer2/.w2` : Sets a timer for '+str(W_TIME)+' minutes and marks washer as TAKEN\n`.washer1 MIN/.w1 MIN/.washer2 MIN/.w2 MIN` : Sets a timer for MIN minutes and marks washer as TAKEN\n`.dryer1/.d1/.dryer2/.d2` : Sets a timer for '+str(D_TIME)+' minutes and marks dryer as TAKEN\n`.dryer1 MIN/.d1 MIN/.dryer2 MIN/.d2 MIN` : Sets a timer for MIN minutes and marks dryer as TAKEN\n\n`.status` : Shows which washers and dryers are currently OPEN/TAKEN\n`.reset MACH` : Resets specified MACH (ALL W1 W2 D1 D2)'
    )

  # .washer1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  if (message.content.startswith('.washer1')):
    W1_TAKEN=getTaken('W1_TAKEN')
    if(W1_TAKEN):
      await message.channel.send(
        atAuthor+'\nThis washer is currently in use by *'+getLastUsed('W1_LAST')+'*'
      )
      return
    else:
      wTime=W_TIME
      # Check for custom_min argument
      if (len(message.content)>len('.washer1')):
        try:
          wTime = int(message.content.split('.washer1',1)[1].strip())
        except ValueError:
          await message.channel.send(
            atAuthor+'\nPlease enter the custom number of minutes as an integer'
          )
          return
      await message.channel.send(
        atAuthor+'\nI will remind you in '+str(wTime)+' minutes!'
      )
      setTaken('W1_TAKEN', True)
      setLastUsed('W1_LAST', message.author.name)
      await asyncio.sleep(wTime * 60)
      # If TAKEN value was reset after calling function
      #if(not getTaken('W1_TAKEN')):
      #  return
      await washer(message.channel, atAuthor, 1)
      return

  # .washer2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  if (message.content.startswith('.washer2')):
    W2_TAKEN=getTaken('W2_TAKEN')
    if(W2_TAKEN):
      await message.channel.send(
        atAuthor+'\nThis washer is currently in use by *'+getLastUsed('W2_LAST')+'*'
      )
      return
    else:
      wTime=W_TIME
      # Check for custom_min argument
      if (len(message.content)>len('.washer2')):
        try:
          wTime = int(message.content.split('.washer2',1)[1].strip())
        except ValueError:
          await message.channel.send(
            atAuthor+'\nPlease enter the custom number of minutes as an integer'
          )
          return
      await message.channel.send(
        atAuthor+'\nI will remind you in '+str(wTime)+' minutes!'
      )
      setTaken('W2_TAKEN', True)
      setLastUsed('W2_LAST', message.author.name)
      await asyncio.sleep(wTime * 60)
      # If TAKEN value was reset after calling function
      #if(not getTaken('W2_TAKEN')):
      #  return
      await washer(message.channel, atAuthor, 2)
      return

  # .dryer1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  if (message.content.startswith('.dryer1')):
    D1_TAKEN=getTaken('D1_TAKEN')
    if(D1_TAKEN):
      await message.channel.send(
        atAuthor+'\nThis dryer is currently in use by *'+getLastUsed('D1_LAST')+'*'
      )
      return
    else:
      dTime=D_TIME
      if (len(message.content)>len('.dryer1')):
        try:
          dTime = int(message.content.split('.dryer1',1)[1].strip())
        except ValueError:
          await message.channel.send(
            atAuthor+'\nPlease enter the custom number of minutes as an integer'
          )
          return
      await message.channel.send(
        atAuthor+'\nI will remind you in '+str(dTime)+' minutes!'
      )
      # Set machine as taken and save name
      setTaken('D1_TAKEN', True)
      setLastUsed('D1_LAST', message.author.name)
      await asyncio.sleep(dTime * 60)
      # If TAKEN value was reset after calling function
      #if(not getTaken('D1_TAKEN')):
      #  return
      await dryer(message.channel, atAuthor, 1)
      return

  # .dryer2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  if (message.content.startswith('.dryer2')):
    D2_TAKEN=getTaken('D2_TAKEN')
    if(D2_TAKEN):
      await message.channel.send(
        atAuthor+'\nThis dryer is currently in use by *'+getLastUsed('D2_LAST')+'*'
      )
      return
    else:
      dTime=D_TIME
      if (len(message.content)>len('.dryer2')):
        try:
          dTime = int(message.content.split('.dryer2',1)[1].strip())
        except ValueError:
          await message.channel.send(
            atAuthor+'\nPlease enter the custom number of minutes as an integer'
          )
          return
      await message.channel.send(
        atAuthor+' I will remind you in '+str(dTime)+' minutes!'
      )
      setTaken('D2_TAKEN', True)
      setLastUsed('D2_LAST', message.author.name)
      await asyncio.sleep(dTime * 60)
      # If TAKEN value was reset after calling function
      #if(not getTaken('D2_TAKEN')):
      #  return
      await dryer(message.channel, atAuthor, 2)
      return

  # .w1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  if (message.content.startswith('.w1')):
    W1_TAKEN=getTaken('W1_TAKEN')
    if(W1_TAKEN):
      await message.channel.send(
        atAuthor+'\nThis washer is currently in use by *'+getLastUsed('W1_LAST')+'*'
      )
      return
    else:
      wTime=W_TIME
      # Check for custom_min argument
      if (len(message.content)>len('.w1')):
        try:
          wTime = int(message.content.split('.w1',1)[1].strip())
        except ValueError:
          await message.channel.send(
            atAuthor+'\nPlease enter the custom number of minutes as an integer'
          )
          return
      await message.channel.send(
        atAuthor+'\nI will remind you in '+str(wTime)+' minutes!'
      )
      setTaken('W1_TAKEN', True)
      setLastUsed('W1_LAST', message.author.name)
      await asyncio.sleep(wTime * 60)
      # If TAKEN value was reset after calling function
      #if(not getTaken('W1_TAKEN')):
      #  return
      await washer(message.channel, atAuthor, 1)
      return

  # .w2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  if (message.content.startswith('.w2')):
    W2_TAKEN=getTaken('W2_TAKEN')
    if(W2_TAKEN):
      await message.channel.send(
        atAuthor+'\nThis washer is currently in use by *'+getLastUsed('W2_LAST')+'*'
      )
      return
    else:
      wTime=W_TIME
      # Check for custom_min argument
      if (len(message.content)>len('.w2')):
        try:
          wTime = int(message.content.split('.w2',1)[1].strip())
        except ValueError:
          await message.channel.send(
            atAuthor+'\nPlease enter the custom number of minutes as an integer'
          )
          return
      await message.channel.send(
        atAuthor+'\nI will remind you in '+str(wTime)+' minutes!'
      )
      setTaken('W2_TAKEN', True)
      setLastUsed('W2_LAST', message.author.name)
      await asyncio.sleep(wTime * 60)
      # If TAKEN value was reset after calling function
      #if(not getTaken('W2_TAKEN')):
      #  return
      await washer(message.channel, atAuthor, 2)
      return

  # .d1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  if (message.content.startswith('.d1')):
    D1_TAKEN=getTaken('D1_TAKEN')
    if(D1_TAKEN):
      await message.channel.send(
        atAuthor+'\nThis dryer is currently in use by *'+getLastUsed('D1_LAST')+'*'
      )
      return
    else:
      dTime=D_TIME
      if (len(message.content)>len('.d1')):
        try:
          dTime = int(message.content.split('.d1',1)[1].strip())
        except ValueError:
          await message.channel.send(
            atAuthor+'\nPlease enter the custom number of minutes as an integer'
          )
          return
      await message.channel.send(
        atAuthor+'\nI will remind you in '+str(dTime)+' minutes!'
      )
      # Set machine as taken and save name
      setTaken('D1_TAKEN', True)
      setLastUsed('D1_LAST', message.author.name)
      await asyncio.sleep(dTime * 60)
      # If TAKEN value was reset after calling function
      #if(not getTaken('D1_TAKEN')):
      #  return
      await dryer(message.channel, atAuthor, 1)
      return

  # .d2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  if (message.content.startswith('.d2')):
    D2_TAKEN=getTaken('D2_TAKEN')
    if(D2_TAKEN):
      await message.channel.send(
        atAuthor+'\nThis dryer is currently in use by *'+getLastUsed('D2_LAST')+'*'
      )
      return
    else:
      dTime=D_TIME
      if (len(message.content)>len('.d2')):
        try:
          dTime = int(message.content.split('.d2',1)[1].strip())
        except ValueError:
          await message.channel.send(
            atAuthor+'\nPlease enter the custom number of minutes as an integer'
          )
          return
      await message.channel.send(
        atAuthor+' I will remind you in '+str(dTime)+' minutes!'
      )
      setTaken('D2_TAKEN', True)
      setLastUsed('D2_LAST', message.author.name)
      await asyncio.sleep(dTime * 60)
      # If TAKEN value was reset after calling function
      #if(not getTaken('D2_TAKEN')):
      #  return
      await dryer(message.channel, atAuthor, 2)
      return

  # .status ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  if (message.content.startswith('.status')):
    await status(message.channel, atAuthor)

  # .reset ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  if (message.content.startswith('.reset')):
    # Sets admin-only
    #if (not atAuthor in ADMINS): return
    whichMach = message.content.split('.reset', 1)[1].lower().strip()
    if (whichMach=='all'):
      await reset(message.channel, atAuthor, 'ALL')
    elif (whichMach=='w1'):
      await reset(message.channel, atAuthor, 'W1_TAKEN')
    elif (whichMach=='w2'):
      await reset(message.channel, atAuthor, 'W2_TAKEN')
    elif (whichMach=='d1'):
      await reset(message.channel, atAuthor, 'D1_TAKEN')
    elif (whichMach=='d2'):
      await reset(message.channel, atAuthor, 'D2_TAKEN')
    else:
      await message.channel.send(
        atAuthor+'\nPlease enter one of the following: \n`ALL W1 W2 D1 D2`'
      )
    return

  # -- Admin-only commands
  if (not atAuthor in ADMINS):
      return

  # - Sends message as bot
  if (message.content.startswith('.sendasbot laundry')):
    msg=message.content.split('.sendasbot laundry',1)[1]
    await client.get_channel(CHANNEL_ID).send(msg)
    return
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~ COMMANDS ~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@client.event
async def washer(channel, atAuthor, num):
  if(num==1):
    setTaken('W1_TAKEN', False)
  elif(num==2):
    setTaken('W2_TAKEN', False)
  msg=atAuthor+'\nYour laundry is done in Washer '+str(num)+'!\n*💡 Please turn off the light on your way out 💡*'
  await channel.send(msg)
  return

@client.event
async def dryer(channel, atAuthor, num):
  # Set machine to OPEN
  if(num==1):
    setTaken('D1_TAKEN', False)
  elif(num==2):
    setTaken('D2_TAKEN', False)
  # Send notification
  msg=atAuthor+' Your laundry is done in Dryer '+str(num)+'!\n*💡 Please clean the lint trap and turn off the light on your way out 💡*'
  await channel.send(msg)
  return

@client.event
async def status(channel, atAuthor):
  W1_TAKEN = getTaken('W1_TAKEN'); W2_TAKEN = getTaken('W2_TAKEN')
  D1_TAKEN = getTaken('D1_TAKEN'); D2_TAKEN = getTaken('D2_TAKEN')
  W1_LAST = getLastUsed('W1_LAST'); W2_LAST = getLastUsed('W2_LAST')
  D1_LAST = getLastUsed('D1_LAST'); D2_LAST = getLastUsed('D2_LAST')
  msg=atAuthor+'\n__Current status of the laundry:__\n'
  if(W1_TAKEN):
    msg+='Washer 1: **TAKEN** by *'+W1_LAST+'*\n'
  else:
    msg+='Washer 1: **OPEN** (last used by *'+W1_LAST+'*)\n'
  if(W2_TAKEN):
    msg+='Washer 2: **TAKEN** by *'+W2_LAST+'*\n'
  else:
    msg+='Washer 2: **OPEN** (last used by *'+W2_LAST+'*)\n'
  if(D1_TAKEN):
    msg+='Dryer 1: **TAKEN** by *'+D1_LAST+'*\n'
  else:
    msg+='Dryer 1: **OPEN** (last used by *'+D1_LAST+'*)\n'
  if(D2_TAKEN):
    msg+='Dryer 2: **TAKEN** by *'+D2_LAST+'*'
  else:
    msg+='Dryer 2: **OPEN** (last used by *'+D2_LAST+'*)'
  await channel.send(msg)
  return


@client.event
async def reset(channel, atAuthor, whichOne):
  if (whichOne=='ALL'):
    for key in ['W1_TAKEN','W2_TAKEN','D1_TAKEN','D2_TAKEN']:
      setTaken(key, False)
    await channel.send(
      atAuthor+' Successfully reset **ALL** taken values'
    )
    print('-- Successfully reset ALL taken values')
  else:
    setTaken(whichOne, False)
    await channel.send(
      atAuthor+' Successfully reset **'+whichOne+'** value'
    )
    print('-- Successfully reset '+whichOne+' value')
  return
# --------------------------------------------------------

# Get taken booleans
def getTaken(key):
  taken=db[key]
  return taken

# Set taken booleans
def setTaken(key, value):
  db[key]=value
  return

# Get last used
def getLastUsed(key):
  lastUsed=db[key]
  return lastUsed

# Set last used
def setLastUsed(key, name):
  db[key]=name
  return

# Pings bot to run continuously
keep_alive()
# Gets secret Discord bot token
client.run(os.environ['TOKEN'])