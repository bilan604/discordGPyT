import os
import re
import asyncio
import time
import random
import discord
from discord.ext import commands
from datetime import datetime
from openAI import askOpenAI003

from dotenv import load_dotenv
load_dotenv()
import tracemalloc
tracemalloc.start()


class DiscordGPT(object):
    def __init__(self, intents=None, command_prefix="/", bot=None) -> None:
        self.intents = intents
        self.command_prefix = command_prefix
        self.bot = bot
        self.quirks = ["(with spectacular rizz)", "Beepp boop bap boop", "Whirrr", "Initiating self destruct sequence (in approximately 60 years)", ""]
        self.last_time = datetime.now()
        self.message_time_stack = [datetime.now()]
        self.ghost = False
        self.team_red = False
        self.intitialize()
    
    def intitialize(self):
        if not self.intents:
            intents = discord.Intents(
                messages=True,
                guilds=True,
                message_content=True
            )
            intents.reactions = True
            self.intents = intents
        
        if not self.bot:
            bot = commands.Bot(
                intents=self.intents,
                author_id=948372828292521984,
                command_prefix=self.command_prefix,
                # Case insensitive
                case_insensitive=True, 
            )
            self.bot = bot
        
        return

    def run(self, bot_token):
        bot = self.bot
        bot_token = bot_token
        
        @bot.event
        async def on_ready():
            print(f"discordGPT bot {bot.user.name} is online")

        @bot.listen()
        async def on_message(message: discord.Message):
            if self.ghost:
                print("GHOSTING BC SPAM")
                return
            if message.author == bot.user:
                return
        
            if len(message.content) >= 1 and message.content[0] == self.command_prefix:
                return
            
            current_time = datetime.now()
            diff1 = current_time-self.last_time
            secondsSinceLastMessage = self.getSeconds(diff1)
            if secondsSinceLastMessage < 3:
                print("Recieved spam", secondsSinceLastMessage)
                return
            
            if len(self.message_time_stack) >= 10:
                stackFirstTime = self.message_time_stack[0]
                diff2 = current_time-stackFirstTime
                secondsForStack = self.getSeconds(diff2)
                if secondsForStack < 150:
                    print("StackSpam", secondsForStack)
                    if secondsForStack < 20:
                        self.ghost = True
                        time.sleep(100000)
                    return
                self.message_time_stack.append(current_time)
                self.message_time_stack = self.message_time_stack[1:]

            else:
                self.message_time_stack.append(current_time)
            
            ctx = await self.bot.get_context(message)
            response = await askOpenAI003(message.content)
            print("RESP", response)

            response = response[:min(4095, len(response))]
            await ctx.send(response)

        @bot.command()
        async def ok(ctx):
            quirk = ""
            if self.quirks:
                quirk = self.quirks[random.randint(0, len(self.quirks)-1)]

            await ctx.send("Hi! " + quirk)

        @bot.command()
        async def whirrr(ctx, *, kwargs):
            await ctx.send("I can't believe that @bot.commands() can't NOT have async await (and whats even worse is that they call it a coroutine!)")
        
        @bot.command()
        async def nap(ctx, *, kwargs):
            time.sleep(100000)
            await ctx.send("Owie")
        
        @bot.command()
        async def summarizeVideo(ctx, *, kwargs):
            video_id = kwargs
            if "v=" in kwargs:
                video_id = kwargs.split("v=")[1]

            transcriptData = YouTubeTranscriptApi.get_transcript(video_id)
            words_in_video = " ".join([item["text"] for item in transcriptData])
            print(f"{len(words_in_video)=}")
            if len(words_in_video.split(" ")) >= 2000:
              words_in_video = " ".join(words_in_video.split(" ")[:2000])
            
            words_in_video = re.sub("\n", " ", words_in_video)
            prompt = "Please create a summary of the following voice-to-text transcript of an educational Youtube video:\n\n"
            prompt += "\"\"\"" + words_in_video + "\"\"\"\n\n"
            summary = await askOpenAI003(prompt)
            await ctx.send(summary)
        @bot.command()
        async def magicTrick(ctx, *, kwargs):
            tricks = True
            if tricks:
                return
            self.doLiteralMagicTrick()
            await ctx.send("Abracadabra")
          
        bot.run(bot_token)


    def getSeconds(self, timeDiff):
        timeDiff = str(timeDiff)
        hours, minutes, seconds =[val for val in timeDiff.split(":")]
        if "." in seconds:
            seconds = seconds.split(".")[0]
        
        return int(seconds) + (60*int(minutes)) + (3600*int(hours))
        
  
    def doLiteralMagicTrick(self):
        # It gives it more personality
        if self.is_hacker:
            return
        if not self.is_hacker:
            return
        return

