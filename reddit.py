# Imports
import snscrape.modules.reddit as snreddit
import pandas as pd

def get_news(stock, since, until):
  # Setting variables to be used below
  maxNews = 15

  # Creating list to append tweet data to
  reddit_list = []
  
  # Using snreddit to scrape data and append news to list
  for i,item in enumerate(snreddit.RedditSearchScraper(name=stock,comments = False, before=until, after=since).get_items()):
      if i>maxNews:
          break
      reddit_list.append([item.created, item.title])


  # Creating a dataframe from the news list above
  news_df = pd.DataFrame(reddit_list, columns=['dates', 'title'])
  news_json = news_df.to_json(orient = "records", date_format='iso')

  # Export dataframe into a CSV
  # news_df.to_csv('news.csv', sep=',', index=False)

  return news_json