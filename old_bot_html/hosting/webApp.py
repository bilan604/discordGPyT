import os
import re
from flask import Markup
import openai
from threading import Thread
from flask import Flask , request
from flask import redirect
from flask import render_template, url_for
from hosting.FlaskServer import askOpenAI


def initializeWebApp(__name__):
  from handling.chatGPT import generate_response

  app = Flask(__name__)
  openai.api_key = os.getenv("OPENAI_API_KEY")

  print("App created!")
  @app.route("/", methods=("GET", "POST"))
  def index():
      if request.method == "POST":
        query = request.form["query"]
        """
        response = openai.Completion.create(
            model="text-davinci-002",  # 002
            prompt=generate_response(query),
            temperature=0.6,
            max_tokens=850
        )
        """
        response = "Your query was: " + query
        return redirect(url_for("index", result=response.choices[0].text))
      else:
        result, result_test = "", ""
      return render_template("index.html", result=result, result_test=result_test)  # re-renders the element


  return app