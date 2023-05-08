import os
import openai
from VideoProcessor import VideoProcessor
from discordGPT import DiscordGPT
from dotenv import load_dotenv

load_dotenv()
import tracemalloc

tracemalloc.start()


def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    bot_token = os.getenv("DISCORD_BOT_SECRET_TOKEN")
    print("BTT:",bot_token)
    discordBot = DiscordGPT()
    discordBot.run(bot_token)

if __name__ == "__main__":
    main()
  
  



