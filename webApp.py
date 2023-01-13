import os
import openai
from threading import Thread
from flask import Flask , request
from flask import redirect
from flask import render_template, url_for
from hosting.FlaskServer import askOpenAI


def initializeWebApp(__name__):
  from handling.chatGPT import generate_response

  appx = Flask(__name__)
  openai.api_key = os.getenv("OPENAI_API_KEY")
  print("App created!")

  @appx.route("/", methods=("GET", "POST"))
  def index():
      if request.method == "POST":
        query = request.form["query"]
        response = openai.Completion.create(
            model="text-davinci-002",  # 002
            prompt=generate_response(query),
            temperature=0.6,
            max_tokens=850
        )
        return redirect(url_for("index", result=response.choices[0].text))

      # "GET" request: Update the HTML page to display the response
      result = " "
      
      # make connect 4!
      #result_test = "Show ConnectFour"
      result_test = "<div>||_||_||_||_||_||_||_||</div>\n"+"<div>||_||_||_||_||_||_||_||</div>\n"+"<div>||_||_||_||_||_||_||_||</div>\n"+"<div>||_||_||_||_||_||_||_||</div>\n"+"<div>||_||_||0||_||_||_||_||</div>\n"+"<div>||x||0||x||_||_||_||_||</div>\n"+"<div>-----------------------</div>\n"+"<div>||0||1||2||3||4||5||6||</div>"

      # HTML will check if result_string is not null and if so, 
      return render_template("index.html", result=result, result_test=result_test)  # re-renders the element

  return appx