import time
import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def getTweet(card):
    username = card.find_element_by_xpath('.//span').text
    handle = card.find_element_by_xpath('.//span[contains(text(),"@")]').text
    try:
        postdate = card.find_element_by_xpath('.//time').get_attribute(
            'datetime')
    except NoSuchElementException:
        return
    comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    text = comment + responding
    reply_count = card.find_element_by_xpath(
        './/div[@data-testid="reply"]').text
    retweet_count = card.find_element_by_xpath(
        './/div[@data-testid="retweet"]').text
    like_count = card.find_element_by_xpath('.//div[@data-testid="like"]').text

    tweet = (username, handle, postdate, text, reply_count, retweet_count,
             like_count)
    print(tweet)
    return tweet


browser = webdriver.Firefox()
browser.get("https://twitter.com/login")
time.sleep(5)
userName = "fantastic4ce"
browser.find_element_by_name("text").send_keys(userName)
browser.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[6]/div/span/span').click()
time.sleep(2)
password = "asimbajwa7"
browser.find_element_by_name("password").send_keys(password)
browser.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div').click()
time.sleep(2)

browser.find_element_by_xpath('/html/body/div/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]').click()
time.sleep(2)

search_input = browser.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/div/div/label/div[2]/div/input')
search_input.send_keys('#BTC')
search_input.send_keys(Keys.RETURN)
time.sleep(3)
##Latest Tab
##browser.find_element_by_link_text('Latest').click()

data = []
tweet_ids = set()
last_position = browser.execute_script("return window.pageYOffset;")
scrolling = True

while scrolling:
    page_cards = browser.find_elements_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/section')
    for card in page_cards[-20:]:
        tweet = getTweet(card)
        if tweet:
            tweet_id = ''.join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                data.append(tweet)
    scroll_attempt = 0
    # print(data)
    while True:
        browser.execute_script(
            'window.scrollTo(0,document.body.scrollHeight);')
        sleep(1)
        current_position = browser.execute_script("return window.pageYOffset;")
        if last_position == current_position:
            scroll_attempt += 1

            if scroll_attempt >= 4:
                scrolling = False
                break
            else:
                sleep(2)
        else:
            last_position = current_position
            break

with open('tweet_data.csv', 'w', newline='', encoding='utf-8') as f:
    header = [
        'Username', 'Handle', 'TimeStamp', 'Comments', 'Likes', 'Retweets',
        'Text'
    ]
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)
