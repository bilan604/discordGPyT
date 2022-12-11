


import os
import json
import openai
import discord
from discord.ext import commands
from random import randint
from FlaskServer import OpenAIServer
from FlaskServer import askOpenAI

from Handler.DataHandler import DB
from utilities import convertWord
from utilities import checkCode

from dotenv import load_dotenv
load_dotenv()

import tracemalloc
tracemalloc.start()


intents = discord.Intents(
  messages=True,
  guilds=True
)
intents.reactions = True


global bot
bot = commands.Bot(
  intents=intents,
  author_id = 948372828292521984,
  command_prefix="/",  # Choose a way to call bot.command() commands
  case_insensitive=True  # Commands aren't case-sensitive
)

@bot.event 
async def on_ready():
    # Prints the bot's username and identifier
    print("@bot.event ready", bot.user, "\n")

client = discord.Client(intents=intents)
#client.run(os.getenv('DISCORD_BOT_SECRET_TOKEN'))

@bot.event
async def on_message(message):
  print(message, "!!!!", message.author, client.user)
  print(message.content)
  print(message.created_at)
  print(message.author.name)
  if message.author == client.user:
    return
  elif message.content.startswith('_'):
    cmd = message.content.split()[0].replace("_","")
    if len(message.content.split()) > 1:
      parameters = message.content.split()[1:]
      print(parameters)