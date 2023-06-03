import os
import openai
from src.parsing import load_credentials
from discordBot.discordGPyT import DiscordGPyT
import tracemalloc
tracemalloc.start()



def main():
    os.chdir("c:/Users/bill/github/DiscordGPyT")
    credentials = load_credentials()
    
    OPENAI_API_KEY = credentials['OPENAI_API_KEY']
    openai.api_key = OPENAI_API_KEY
    
    bot_token = credentials['DISCORD_BOT_SECRET_TOKEN']

    discordBot = DiscordGPyT()
    discordBot.run(bot_token)



if __name__ == "__main__":
    main()

  



