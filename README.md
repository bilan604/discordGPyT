# OpenAI-discord-autobot

This repo contains a Discord Bot/AI that can answer questions in Discord with responses from GPT3's newest language model (chatGPT).  
1. It allows you to use Discord chat as smart Compiler for Python3, Java, and C++ using /Python3, /Java, and /CPP.  
2. It can also code itself with a command injection check bypass (generateCommands function).  
3. It hosts a Flask Server making the API requests, and an interface written in HTML that can be alternatively used to query GPT3.  

https://user-images.githubusercontent.com/77251582/207458277-081d419f-078e-45b7-ac70-b13433962d54.mp4
![screenshot](https://github.com/bilan604/OpenAI-Discord-autobot/blob/master/static/JavaPythonCPP.png?width=20x)  
![screenshot](https://github.com/bilan604/OpenAI-Discord-autobot/blob/master/static/Python-OpenAI.png?width=20px)  

## App.py
The bot and bot commands. Message sent in Discord chat beggining with "/" call bot commands.  

This bot supports GPT queries with the command /AI *prompt*, where-in the bot will repond with GPT3's output. It also has various commands that use GPT3 such as /summarize, which summarizes text.  

Within the command functionalities, this bot/AI can run code given directly from the Discord chat, as well as inject commands into itself using a command injection bypass. More interestingly, since the bot supports GPT3 and Command Injection, the bot can code itself, which is initiated with the /generateCommands function. It will use GPT3 to generate some commands it could code, then use GPT3 to code out the commands, before the code is injected into the bot itself.


## FlaskServer.py  
Implements the OpenAI API and currently uses the Davinci-003 (the new GPT3).  

The Flask server itself hosts the GPT3 connection, and operates a website that can handle GPT3 queries in a text-entry box. The bot uses (pings) this Flask server, which keeps its instance alive.  

## .env file not included in repo because it contains the Discord/OpenAI authentication tokens  

