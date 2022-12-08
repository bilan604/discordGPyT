import os
import random

import openai

from threading import Thread
from flask import Flask, redirect, render_template, request, url_for
from dotenv import load_dotenv


def OpenAIServer():  
  global app
  app = Flask(__name__)

  load_dotenv()
  openai.api_key = os.getenv("OPENAI_API_KEY")
  print("App created")
  
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
  
  
  def run():
    print("----Flask App run() function run")
    app.run(
  		host='0.0.0.0',
  		port=random.randint(2000,9000)
  	)
  
  def OpenAIServer():
    '''
  	Creates and starts new thread that runs the function run.
    Keeps the bot alive by continueously pinging
  	'''
    t = Thread(target=run)
    t.start()
  
  prompt_general = """{}"""
  
  
  def generate_response(query):
      return prompt_general.format(
          query.capitalize()
      )
  
def askOpenAI(query):
  # text-davinci-002
  global app, openai
  response = openai.Completion.create(
              model="text-davinci-003",
              prompt=query,
              temperature=0.5,
              max_tokens=800
            )
  return response.choices[0].text