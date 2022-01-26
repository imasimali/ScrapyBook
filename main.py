from flask import Flask, request, redirect, url_for, jsonify, json
import pandas as pd
import os
import time
import requests
import twitter
import subprocess

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/')
def hello_world():
  return '<h1>Hello, World!</h1>'

@app.route("/twitter")
def scrape_twitter():
    stock = request.args["stock"]
    since = request.args["since"]
    until = request.args["until"]
    tweets = twitter.get_tweets(stock,since,until)
    tweets_json = json.loads(tweets)
    return jsonify(tweets_json)

@app.route("/getyahoo")
def scrape_yahoo():
    stock = request.args["stock"]
    filename = time.strftime("%d%H%M%S")
    subprocess.run('cd yahoo && scrapy crawl yh -a code='+stock+' -o '+filename+'.json && cd ..', shell=True)
    df = pd.read_json('yahoo/'+filename+'.json')
    df1 = json.loads(df.to_json(orient = "index"))
    return jsonify(df1)

app.run(host='0.0.0.0', port=8080)