import os
import json
import openai
import discord
from random import randint
from discord.ext import commands
from hosting.FlaskServer import OpenAIServer
from hosting.FlaskServer import askOpenAI

from handling.DataHandler import DB
from handling.utilities import convertWord
from handling.utilities import checkCode

from dotenv import load_dotenv
load_dotenv()

import tracemalloc
tracemalloc.start()


intents = discord.Intents(
  messages=True,
  guilds=True
)
intents.reactions = True

command_prefix = "/"


global bot
bot = commands.Bot(
  intents=intents,
  author_id = 948372828292521984,
	command_prefix=command_prefix,  # Choose a way to call bot.command() commands
	case_insensitive=True  # Commands aren't case-sensitive
)


@bot.event 
async def on_ready():
    # Prints the bot's username and identifier
    print("@bot.event ready", bot.user, "\n")

@bot.listen()
async def on_message(message: discord.Message):
    # if the message is from the bot itself
    if message.author == bot.user:
      return
    
    # "context determines the purpose of Statistical work"
    ctx = await bot.get_context(message)

    # otherwise its just a message
    global db
    db.addMessage(message)


"""
#########################################################
Bot Commands:
#########################################################
"""

@bot.command()
async def ok(ctx):
  await ctx.send("Bot is Online!")

@bot.command()
async def utter(ctx, s):
  await ctx.send(s)

@bot.command()
async def echo(ctx, *, kwargs):
  await ctx.send(kwargs)

@bot.command()
async def intro(ctx):
  # Introduce self
  introduction = "Hi, I named myself Daisy. I am a Python bot being hosted on a Flask server that\
    interacts with the OpenAI API key. I can execute various commands, execute code written in the\
    Discord chat, and respond to questions/requests with OpenAI's Davinci-003 Natural Language Model.\
    I can also inject commands utilizing an a async injected command check bypass, and thus code myself"
  await ctx.send(introduction)

@bot.command()
async def showInputArray(ctx, *kwargs):
  await ctx.send(kwargs)

@bot.command()
async def reverseInput(ctx, s):
  s = s[::-1]
  await ctx.send(s)

@bot.command()
async def add(ctx, x, y):
  x = int(x)
  y = int(y)
  await ctx.send(x+y)

@bot.command()
async def areEqual(ctx, a, b):
  await ctx.send(a == b)

@bot.command()
async def replacePattern(ctx, *kwargs):
  if len(kwargs) == 1:
    await ctx.send("No words")
    return
  pattern = kwargs[0]
  words = []

  for i in range(1, len(kwargs)):
    words.append(kwargs[i])
  pattern = convertWord(pattern)
  matched_words = []

  for i in range(len(words)):
    if pattern == convertWord(words[i]):
      matched_words.append(words[i])

  await ctx.send("Here are the words that matches pattern" + kwargs[0])
  await ctx.send(matched_words)

@bot.command()
async def executeCode(ctx, *, kwargs):
  global ans
  global s, s1, s2
  global dd, dd1, dd2
  global lst, lst1, lst2

  code = kwargs
  exec(code)
  await ctx.send(ans)

# you don't need comments when you have readability
@bot.command()
async def dc(ctx):
  db.delete_code()

@bot.command()
async def al(ctx, *, kwargs):
  db.add_line(kwargs)

@bot.command()
async def vc(ctx):
  global db
  code = db.get_code()
  await ctx.send(code)

@bot.command()
async def rc(ctx):
  global ans
  global dd, dd1, dd2
  global lst, lst1, lst2
  ans = "ans"

  global db
  code = db.get_code()
  code = checkCode(code)
  exec(code)
  await ctx.send("Code Executed")
  await ctx.send("ans = " + ans)

@bot.command()
async def dice(ctx):
  await ctx.send(randint(1,6))

@bot.command()
async def AI(ctx, *, kwargs):
  response = askOpenAI(kwargs)
  print(response)
  await ctx.send(response)

@bot.command()
async def python(ctx, s):
    exec(s)

@bot.command()
async def addCommands(ctx, *, kwargs):
    global command_names
    kwargs += "Do not name the commands you write any of the following names (" + \
      ",".join(command_names) + ")"
    code = askOpenAI(kwargs)
    await ctx.send("The code OpenAI wrote:\n" + code)
    await python(ctx, code)
    await ctx.send("Commands Added")

@bot.command()
async def generateCommands(ctx):
  raw_query = "Please name and describe 3 useful Commands that a Discord bot implementing the OpenAI API key\
    might find useful. List the commands out in bullet point format. They should follow the format\
    @bot.command()\n \
    async def function_name(ctx, *, kwargs):\n \
      # code here\n \
      await ctx.send(output)"
  query = askOpenAI(raw_query)
  await ctx.send("The query OpenAI wrote for itself:\n" + query)
  code = askOpenAI(query)
  await ctx.send("The code OpenAI wrote:\n" + code)
  await python(ctx, code)
  await ctx.send("Commands Added")


"""
#########################################################
OpenAI's Commands
#########################################################
"""

@bot.command()
async def commandSelf(ctx):
    await ctx.send("Hi, I'm a Discord bot! I'm here to help you out\
    with whatever you need. Let's get started with an introduction.\n")
    await intro(ctx)

@bot.command()
async def addCommand(ctx):
    @bot.command()
    async def sendReaction(ctx):
        await ctx.message.add_reaction('👍')
    await sendReaction(ctx)

@bot.command()
async def sendEmbedMessage(ctx):
    embed = discord.Embed(title="Title", description="This is a description", color=0x00ff00)
    await ctx.send(embed=embed)
@bot.command()
async def removeCommand(ctx, commandName):
    bot.remove_command(commandName)       

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def embed(ctx):
    embed = discord.Embed(title="Example Embed", description="This is an example embed!", color=0x00ff00)
    embed.add_field(name="Field 1", value="This is field 1")
    embed.add_field(name="Field 2", value="This is field 2")
    await ctx.send(embed=embed)

@bot.command()
async def helper(ctx):
    embed = discord.Embed(title="Help", description="These are the commands you can use!", color=0x00ff00)
    embed.add_field(name="addCommand", value="Adds a new command to the bot")
    embed.add_field(name="removeCommand", value="Removes a command from the bot")
    embed.add_field(name="ping", value="Returns 'Pong!'")
    embed.add_field(name="echo", value="Repeats the given message")
    embed.add_field(name="embed", value="Sends an example embed")
    await ctx.send(embed=embed)

@bot.command()
async def translate(ctx, *, kwargs):
    idx = kwargs.index(" ")
    language, input = kwargs[:idx], kwargs[idx+1:]
    output = "Translating the following text into 1." + language + "\n\n1."
    output += askOpenAI(output + input)
    await ctx.send(output)

@bot.command()
async def commands(ctx):
    command_list = [command.name for command in bot.commands]
    await ctx.send('Commands: ' + ', '.join(command_list))


global command_names
command_names = [command.name for command in list(bot.commands)]
print(command_names)

global bot_commands
bot_commands = {command.name: command for command in list(bot.commands)}

@bot.command()
async def invokeOK(ctx):
  for command in list(bot.commands):
    if command.name == 'ok':
      await command.invoke(ctx)

if __name__ == '__main__':
  db = DB()
  server = OpenAIServer()
  bot_token = os.getenv('DISCORD_BOT_SECRET_TOKEN')
  bot.run(bot_token)

