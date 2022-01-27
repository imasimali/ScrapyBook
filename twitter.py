# Imports
import snscrape.modules.twitter as sntwitter
import pandas as pd

def get_tweets(stock,since,until):
  # Setting variables to be used below
  maxTweets = 10

  # Creating list to append tweet data to
  tweets_list = []
  
  # Using TwitterSearchScraper to scrape data and append tweets to list
  for i,tweet in enumerate(sntwitter.TwitterSearchScraper(stock+' since:'+ since + ' until:'+ until +' lang:en').get_items()):
      if i>maxTweets:
          break
      tweets_list.append([tweet.date, tweet.content])

  # Creating a dataframe from the tweets list above
  tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Text'])
  tweets_json = tweets_df.to_json(orient = "index",date_format='iso')

  # Export dataframe into a CSV
  # tweets_df.to_csv('tweets.csv', sep=',', index=False)

  return tweets_json