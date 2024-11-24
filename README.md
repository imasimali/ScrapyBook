# ScrapyBook: News Data Scraping and REST API Service

This repository contains the code for ScrapyBook, a powerful tool built to scrape news data from multiple sources including Twitter, Yahoo Finance, Reuters, and Reddit. It provides a seamless interface to access the scraped data via a Flask-based REST API.

## Core Functionality
- **News Scraping:** Collects real-time news data from:
    - Twitter: Financial trends and tweets.
    - Yahoo Finance: Stock-related news and updates.
    - Reuters: Breaking news and market insights.
    - Reddit: Relevant discussions and sentiment from financial communities.

- **Flask API:** Exposes the scraped data via RESTful endpoints for easy integration with external systems.
- **Selenium Integration:** Handles dynamic websites requiring JavaScript rendering for accurate scraping.


## Technical Stack
- **Web Scraping:** Built using Scrapy for efficient and scalable scraping.
- **Dynamic Content Handling:** Utilizes Selenium for scraping JavaScript-rendered content.
- **Backend Framework:** Flask for serving data through a REST API.

