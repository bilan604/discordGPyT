# A completely different, newer version of the bot has been made. It has been refactored to a class and can do cool things like summarize youtube videos. https://replit.com/@Xing-YangYang1/discordGPT?v=1  

## ![screenshot](https://github.com/bilan604/OpenAI-Discord-autobot/blob/master/static/SeaTurtlePNG.png?width=20px)  

# V2: OpenAI-discord-autobot

This repo contains a Discord Bot/AI implements the chatGPT API for various functions. The Discord bot started as a bot that could act as a compiler through Discord chat, and throughout its development, I discovered a command injection vulnerability (seriously). The bot used to be able to code itself with this command injection bypass, but the developers have since fixed this issue/feature (breaking the functions that allowed the bot to add code to itself).

The bot:
1. It allows you to use Discord chat as smart Compiler for Python3, Java, and C++ using /Python3, /Java, and /CPP.  
2. [No longer supported] It can also code itself with a command injection check bypass (generateCommands function).  
3. Various commands such as /summarize, which summarizes text.  


## the bot creating and adding the /help command to itself
## ![screenshot](https://github.com/bilan604/OpenAI-Discord-autobot/blob/master/static/generateCommands-Discord-AI.png?width=20px)  


https://user-images.githubusercontent.com/77251582/207458277-081d419f-078e-45b7-ac70-b13433962d54.mp4


# V1:
## App.py
The bot and bot commands. Message sent in Discord chat beggining with "/" call bot commands.  

[No longer supported] Within the command functionalities, this bot/AI can run code given directly from the Discord chat, as well as inject commands into itself using a command injection bypass. More interestingly, since the bot supports GPT3 and Command Injection, the bot can code itself, which is initiated with the /generateCommands function. It will use GPT3 to generate some commands it could code, then use GPT3 to code out the commands, before the code is injected into the bot itself.


## FlaskServer.py: The flask server  
While developing the Discord bot, I used to keep the bot online by making ping requests every five minutes to a Flask Server. The Flask Server is now used to make chatGPT API requests. Since I needed the Flask Server anyways, I implemented the chatGPT API into a small web application and wrote some JavaScript to add visual effects to the web app. As of now, the Flask Server is no longer needed.  
Implements the OpenAI chatGPT API and currently uses the Davinci-003 (the new GPT3).  

The Flask server itself hosts the GPT3 connection, and operates a website that can handle GPT3 queries in a text-entry box. The bot uses (pings) this Flask server, which keeps its instance alive.  

## .env file not included in repo because it contains the Discord/OpenAI authentication tokens  

