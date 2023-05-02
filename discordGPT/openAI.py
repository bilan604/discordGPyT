import os
import openai
import time
from dotenv import load_dotenv
load_dotenv()


async def askOpenAI003(query):
  message = "[Empty Message]"
  try:
    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=query,
                                        temperature=0.35,
                                        max_tokens=1000)
    message = response.choices[0].text
    time.sleep(2)
  except Exception as e:
    print(e)

  time.sleep(2)
  return message
