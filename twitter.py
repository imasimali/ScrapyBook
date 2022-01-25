# Imports
import snscrape.modules.twitter as sntwitter
import pandas as pd

# Setting variables to be used below
maxTweets = 50

# Creating list to append tweet data to
tweets_list = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('aapl since:2022-01-25 until:2022-01-26').get_items()):
    if i>maxTweets:
        break
    tweets_list.append([tweet.date, tweet.content])

# Creating a dataframe from the tweets list above
tweets_df2 = pd.DataFrame(tweets_list, columns=['Datetime', 'Text'])

# Display first 5 entries from dataframe
tweets_df2.head()

# Export dataframe into a CSV
tweets_df2.to_csv('text-query-tweets.csv', sep=',', index=False)