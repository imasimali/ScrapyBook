# Imports
import snscrape.modules.reddit as snreddit
import pandas as pd

def get_tweets(stock='aapl',since='2022-01-25',until='2022-01-26'):
  # Setting variables to be used below
  maxNews = 10

  # Creating list to append tweet data to
  reddit_list = []
  
  # Using RedditSearchScraper to scrape data and append news to list
  for i,tweet in enumerate(snreddit.RedditSearchScraper(stock+' since:'+ since + 'until:'+ until)):
      if i>maxNews:
          break
      reddit_list.append([tweet.date, tweet.content])

  # Creating a dataframe from the tweets list above
  tweets_df = pd.DataFrame(reddit_list, columns=['Datetime', 'Text'])
  tweets_json = tweets_df.to_json(orient = "index")

  # Export dataframe into a CSV
  # tweets_df.to_csv('tweets.csv', sep=',', index=False)

  return tweets_json

get_tweets()