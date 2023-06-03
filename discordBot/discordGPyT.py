import time
import os
import asyncio
import random
import discord
from discord.ext import commands
from datetime import datetime
from src.askOpenAI import askOpenAI003
from src.parsing import check_spam
from src.helpers import getYoutubePrompt, doGoogleSearch
import tracemalloc
tracemalloc.start()


class DiscordGPyT(object):

    def __init__(self, intents=None, command_prefix="/", bot=None) -> None:
        self.intents = intents
        self.command_prefix = command_prefix
        self.bot = bot
        # Whether the bot replies to messages without a command prefix, i.e. /AI
        self.default_reply = True
        # Messages that would have gotten cuttoff by the character limit
        # are stored here due to loops not being allowed in bot.run async awaits
        # there are some dependency quirks
        self.message_cuttoff_stack = []
        
        # Spam filter. Messages have a cumulative limited rate. 
        self.message_time_stack = [datetime.now()]
        # Time the 10th last message was recieved
        self.last_time = datetime.now()
        # Ignore spam or not
        self.ghost = False
        # Greetings
        self.quirks = [
            "Beepp boop bap boop", "Whirrr", "(with spectacular rizz)",
            "This feature is a reflection of the world around us!",
            "Lots of personality!",
            ""
        ]
        self.intitialize()

    ##########################################
    # called in __init__
    def intitialize(self):
        if not self.intents:
            intents = discord.Intents(messages=True,
                                                                guilds=True,
                                                                message_content=True)
            intents.reactions = True
            self.intents = intents

        if not self.bot:
            bot = commands.Bot(
                intents=self.intents,
                author_id=948372828292521984,
                command_prefix=self.command_prefix,
                case_insensitive=True,
            )
            self.bot = bot
        
        return


    async def sendDiscordMessage(self, message, response=None):
        # can only handle oversized messages if ctx is given

        if response == None:
            # message is a discord message object. message.content is the message string
            ctx = await self.bot.get_context(message)  
            response = message.content
            # possibly oversized
            response, self.message_stack = self.parse_oversized_message(response)
            await ctx.send(response)
        else:
            # message is a discord message object. message.content is the message string
            ctx = await self.bot.get_context(message)  
            # response is what can actually be sent 
            # (i.e. character limit makes response a shorter version)
            # possibly oversized
            response, self.message_stack = self.parse_oversized_message(response)
            await ctx.send(response)
        return

    def parse_oversized_message(self, message):
        # if the bot's message is too long to send
        if len(message) < 1950:
            return message, []
        
        print("oversized response recieved")
        new_stack = []
        for i in range(0, len(message), 1950):
            idx_end = i+1950
            new_stack.append(message[i:min(len(message), idx_end)])
    
        new_message_stack = []
        for new_message in new_stack[1:]:
            print("new Message", len(new_message))
            new_message_stack.append(new_message)
        print("LENGTHS", len(new_stack[0]), len(new_message_stack))
        return new_stack[0], new_message_stack
    
    # run the bot
    def run(self, bot_token):
        bot = self.get_bot(bot_token)
        bot.run(bot_token)

    # Define a bot
    def get_bot(self, bot_token):
        # to do @bot.event declarations
        bot = self.bot
        # Note: A Discord developer bot token is required
        bot_token = bot_token

        ################
        # When the bot boots up
        @bot.event
        async def on_ready():
            print(f"discordGPT bot {bot.user.name} is online")

        ###############
        # The main.py for the bot basically
        # Called for every message received, including its own
        @bot.listen()
        async def on_message(message: discord.Message):
            print("new message recieved")

            if len(message.content) < 1:
                print("Empty message received")
                return

            # variable for ghosting spam
            if self.ghost:
                print("self.ghost - ed")
                return

            # Check if the bot is receiving its own message
            if message.author == bot.user:
                # There is a 2000 character cutoff limit in Discord
                if self.message_cuttoff_stack:
                    next_chunk = self.message_cuttoff_stack.pop()
                    await self.sendDiscordMessage(message, next_chunk)
                
                return

            if message.content[0] == self.command_prefix:
                # Then this is a command. i.e. "/roll"
                # Ignore, otherwise, both GPT and the bot command will occur
                return

            # Check for spam
            self.ghost, self.message_time_stack = check_spam(self.last_time, self.message_time_stack)
            if self.ghost:
                time.sleep(1000000)
                return      

            # Whether to respond to non-chat messages
            if self.default_reply:
                response = await askOpenAI003(message)
                response, self.message_stack = self.parse_oversized_message(response)
                await self.sendDiscordMessage(message, response)
            
            return
        
        bot = self.load_bot_commands(bot)
        return bot

    # creates a set of commands for the bot
    def load_bot_commands(self, bot):
        #########################
        # BOT COMMANDS START HERE
        @bot.command()
        async def ok(ctx):
            quirk = ""
            if self.quirks:
                quirk = self.quirks[random.randint(0, len(self.quirks) - 1)]
            await ctx.send("Hi! " + quirk)

        
        @bot.command()
        async def ai(ctx, *, kwargs):
            if not kwargs:
                print("ai(): Empty kwargs")
                return
            response = await askOpenAI003(kwargs)
            response, self.message_stack = self.parse_oversized_message(response)
            await ctx.send(response)


        @bot.command()
        async def toggleReplies(ctx):
            self.default_reply = not self.default_reply
            if self.default_reply:
                response = "Default replies are now on"
            else:
                response = "Default replies are now off"
            await ctx.send(response)

        
        @bot.command()
        async def Marco(ctx):
            await ctx.send(
                "Polo"
            )

        
        @bot.command()
        async def summarizeVideo(ctx, *, kwargs):
            if not kwargs:
                print("summarizeVideo(): Empty kwargs")
                return
            
            prompt = await asyncio.create_task(getYoutubePrompt(kwargs))
            summary = await askOpenAI003(prompt)
            await ctx.send(summary)

        @bot.command()
        async def search(ctx, *, kwargs):
            if True:
                await ctx.send("This feature is not being going to be implemented due to the vulnerabilities introduced by using chromium")
                return
            if not kwargs:
                return
            if kwargs[-1] != "?":
                kwargs += "?"
            
            response = await asyncio.create_task(doGoogleSearch(kwargs))
            response, self.messageStack = self.parse_oversized_message(response)
            await ctx.send(response)
        
        @bot.command()
        async def magicTrick(ctx, kwargs):
            magic = True
            if magic:
                return
            
            tricks = False
            if not tricks:
                return

            await ctx.send("Abracadabra")

        ###########################
        # After all the functions above are defined, the bot is run
        # this is the last line of the discordGPT.run() function
        return bot
        ###########################
