import os
import random
from dotenv import load_dotenv

import openai

from threading import Thread
from flask import Flask , request
from flask import redirect
from flask import render_template, url_for


def OpenAIServer():  
  global app
  app = Flask(__name__)

  load_dotenv()
  openai.api_key = os.getenv("OPENAI_API_KEY")
  
  print("App created!")
  
  empty_prompt = """{}"""

  @app.route("/", methods=("GET", "POST"))
  def index():
      if request.method == "POST":
          query = request.form["query"]
          response = openai.Completion.create(
              model="text-davinci-002",  # 002
              prompt=generate_response(query),
              temperature=0.6,
              max_tokens=50
          )
          print(f"{response.choices=}")
          return redirect(url_for("index", result=response.choices[0].text))
  
      # "GET" request: Update the HTML page to display the response
      result = request.args.get("result")  # pointer to HTML element to modify
      return render_template("index.html", result=result)  # re-renders the element
  
  def generate_response(query):
      return empty_prompt.format(
          query.capitalize()
      )
  
  def run():
    print("Flask App runing")
    app.run(
  		host='0.0.0.0',
  		port=random.randint(2000,9000)
  	)
  
  def OpenAIServer():
    '''
    Keeps the bot online by continueously pinging
  	'''
    t = Thread(target=run)
    t.start()


def askOpenAI(query):
  global app, openai
  response = openai.Completion.create(
              model="text-davinci-003",
              prompt=query,
              temperature=0.6,
              max_tokens=1200
            )
  return response.choices[0].text

