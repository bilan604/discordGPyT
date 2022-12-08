# discord-OpenAI-autobot

This repo contains a Discord Bot that can code itself.  It is written in Python and implements the OpenAI Davinci-003 Natural Language Model, better known as GPT3. Message sent in Discord chat beggining with "/" call bot commands.  

Within the command functionalities, this bot/AI can run code given directly from the Discord chat, as well as inject commands into itself using a command injection bypass.  
This bot supports GPT queries with the command /OpenAI *prompt*, where-in the bot will repond with GPT3's output. It also has various commands that use GPT3 such as /summarize, which summarizes text.  

More interestingly, since the bot supports GPT3 and Command Injection, the bot can code itself, which is initiated with the /generateCommands function. It will use GPT3 to generate some commands it could code, then use GPT3 to code out the commands, before the code is injected into the bot itself.

The bot is Hosted on (pings) a Flask server, which keep's its instance alive. The Flask server itself hosts the GPT3 connection, and operates a website that can handle GPT3 queries in a text-entry box.  



