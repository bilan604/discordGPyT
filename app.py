import os
import discord
import openai
from discord.ext import commands
from random import randint
from utilities import convertWord
from utilities import checkCode
from FlaskServer import OpenAIServer
from FlaskServer import askOpenAI

from dotenv import load_dotenv

import tracemalloc
tracemalloc.start()


intents =  intents = discord.Intents(messages=True, guilds=True)
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


"""
#########################################################
Bot Commands
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
    I can also inject commands with the code execution, and code myself"
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
  await ctx.send(kwargs)
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
  # what Leetcode does to a Software Developer: Observe
  global ans
  global s, s1, s2
  global dd, dd1, dd2
  global lst, lst1, lst2

  code = kwargs
  exec(code)
  await ctx.send(ans)

@bot.command()
async def dc(ctx, *, kwargs):
  # delete code
  with open("code.txt", "w+") as f:
    pass

@bot.command()
async def al(ctx, *, kwargs):
  with open("code.txt", "a") as f:
    f.write(kwargs + "\n")

@bot.command()
async def vc(ctx):
  # view code
  with open("code.txt", "r") as f:
    await ctx.send("".join(f.readlines()))

@bot.command()
async def rc(ctx):
  global ans
  global s, s1, s2
  global dd, dd1, dd2
  global lst, lst1, lst2
  global dd_self
  ans = "ans"
  with open("code.txt", "r") as f:
    code_lines = f.readlines()
    code = "".join(checkCode(code_lines))
    exec(code)
    await ctx.send("Code Executed")
    await ctx.send("ans = " + ans)

@bot.command()
async def dice(ctx):
  await ctx.send(randint(1,6))

@bot.command()
async def OpenAI(ctx, *, kwargs):
  response = askOpenAI(kwargs)
  await ctx.send(response)

@bot.command()
async def python(ctx, s):
    exec(s)

@bot.command()
async def commandSelf(ctx):
    await ctx.send("Hi, I'm a Discord bot! I'm here to help you out with whatever you need. Let's get started with an introduction.\n")
    await intro(ctx)

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


global command_names
command_names = [command.name for command in list(bot.commands)]

extensions = [
	'cogs.cog_example'
]


if __name__ == '__main__':
  for extension in extensions:
    bot.load_extension(extension)


# Starts a webserver to be pinged
OpenAIServer()

load_dotenv()
bot_token = os.getenv('DISCORD_BOT_SECRET_TOKEN')
bot.run(bot_token)

