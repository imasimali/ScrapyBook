from flask import Flask, request, jsonify, json
import pandas as pd
import time
import twitter
import reddit
import subprocess
import pathlib as p
import shlex

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/')
def hello_world():
  return '<h1>This is ScrapyBook backend!</h1></br><h3>You need commands to scrape!<h3/><h4>Contact Asim for help >> hi@asim.id<h4/>'

@app.route("/twitter")
def scrape_twitter():
    stock = request.args["stock"]
    since = request.args["since"]
    until = request.args["until"]
    tweets = twitter.get_tweets(stock, since, until)
    tweets_json = json.loads(tweets)
    return jsonify(tweets_json)

@app.route("/reddit")
def scrape_reddit():
    stock = request.args["stock"]
    since = request.args["since"]
    until = request.args["until"]
    news = reddit.get_news(stock, since, until)
    news_json = json.loads(news)
    return jsonify(news_json)

@app.route("/yahoo")
def scrape_yahoo():
    stock = request.args["stock"]
    filename = stock+time.strftime("%d")
    path = p.Path('yahoo/'+filename+'.json')
    if not path.exists():
      bashCommand = "scrapy crawl yh -a code="+stock+" -o "+filename+".json"
      process = subprocess.run(shlex.split(bashCommand), cwd=r'yahoo/', stdout=subprocess.PIPE)
    df = pd.read_json('yahoo/'+filename+'.json')
    df1 = json.loads(df.to_json(orient = "records"))
    return jsonify(df1)

@app.route("/reuters")
def scrape_reuters():
    stock = request.args["stock"]
    filename = stock+time.strftime("%d")
    path = p.Path('reuters/'+filename+'.json')
    if not path.exists():
      bashCommand2 = "scrapy crawl rt -a code="+stock+" -o "+filename+".json"
      process = subprocess.run(shlex.split(bashCommand2), cwd=r'reuters/', stdout=subprocess.PIPE)
    df = pd.read_json('reuters/'+filename+'.json')
    df1 = json.loads(df.to_json(orient = "records"))
    return jsonify(df1)

app.run(host='0.0.0.0',port='8080')
