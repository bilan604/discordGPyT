# A completely different, newer version of the bot has been made. It has been refactored to a class and can do cool things like summarize youtube videos. https://replit.com/@Xing-YangYang1/discordGPT?v=1  

## ![screenshot](https://github.com/bilan604/OpenAI-Discord-autobot/blob/master/static/SeaTurtlePNG.png?width=20px)  

Note: You will need your own API tokens from OpenAI and Discord to run this

## The bot creating and adding the /help command to itself
## ![screenshot](https://github.com/bilan604/OpenAI-Discord-autobot/blob/master/static/generateCommands-Discord-AI.png?width=20px)  

https://user-images.githubusercontent.com/77251582/207458277-081d419f-078e-45b7-ac70-b13433962d54.mp4


## FlaskServer.py: The flask server  
While developing the Discord bot, I used to keep the bot online by making ping requests every five minutes to a Flask Server. The Flask Server is now used to make chatGPT API requests. Since I needed the Flask Server anyways, I implemented the chatGPT API into a small web application and wrote some JavaScript to add visual effects to the web app. As of now, the Flask Server is no longer needed.  
Implements the OpenAI chatGPT API and currently uses the Davinci-003 (the new GPT3).  

The Flask server itself hosts the GPT3 connection, and operates a website that can handle GPT3 queries in a text-entry box. The bot uses (pings) this Flask server, which keeps its instance alive.  




