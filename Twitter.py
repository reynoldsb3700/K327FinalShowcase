# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 14:05:11 2020

@author: Blake
"""

import re
from datetime import datetime
from time import sleep
from selenium.webdriver.common.keys import Keys
from msedge.selenium_tools import Edge, EdgeOptions

def get_tweet_data(card):
    """Extract data from tweet card"""
    try:
        username = card.find_element_by_xpath('.//span').text
    except:
        return
    try:
        handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    except:
        return
    
    try:
        postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
        postdate = datetime.strptime(postdate,'%Y-%m-%dT%H:%M:%S.000Z')
        
    except:
        return
    try:
        text = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    except:
        return
    
    # get a string of all emojis contained in the tweet
    """Emojis are stored as images... so I convert the filename, which is stored as unicode, into 
    the emoji character."""
    emoji_tags = card.find_elements_by_xpath('.//img[contains(@src, "emoji")]')
    emoji_list = []
    for tag in emoji_tags:
        filename = tag.get_attribute('src')
        try:
            emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename).group(1), base=16))
        except AttributeError:
            continue
        if emoji:
            emoji_list.append(emoji)
    emojis = ' '.join(emoji_list)
    
    tweet = (username, handle, postdate, text, emojis)
    return tweet

# application variables
user = '5853533613'
my_password = '98827Vcs'
test_list = ['Cam Newton','Derek Carr','Drew Lock']
qb_list = ['Josh Allen','Cam Newton','Sam Darnold','Ryan Fitzpatrick','Derek Carr','Patrick Mahomes','Drew Lock','Justin Herbert','Ben Roethlisberger','Baker Mayfield','Joe Burrow','Lamar Jackson','Ryan Tannehill','Philip Rivers','Deshaun Watson','Gardner Minshew','Daniel Jones','Carson Wentz','Alex Smith','Andy Dalton','Aaron Rodgers','Nick Foles','Mitch Trubisky','Matthew Stafford','Kirk Cousins','Jared Goff','Kyler Murray','Russell Wilson','Jimmy Garoppolo','Tom Brady','Teddy Bridgewater','Matt Ryan','Drew Brees']
search_term = ''
describe_list = ['sucks','great']
data = []
cutoff_date = datetime(2020,9,13)
for x in qb_list:
    for j in describe_list:
        search_term = x+" "+j

# create instance of web driver
        options = EdgeOptions()
        options.use_chromium = True
        driver = Edge(options=options)
        
        # navigate to login screen
        driver.get('https://www.twitter.com/login')
        driver.maximize_window()
        
        username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
        username.send_keys(user)
        
        password = driver.find_element_by_xpath('//input[@name="session[password]"]')
        password.send_keys(my_password)
        password.send_keys(Keys.RETURN)
        sleep(1)
        
        # find search input and search for term
        search_input = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
        search_input.send_keys(search_term)
        search_input.send_keys(Keys.RETURN)
        sleep(1)
        
        # navigate to historical 'latest' tab
        driver.find_element_by_link_text('Latest').click()
        
        # get all tweets on the page
        tweet_ids = set()
        last_position = driver.execute_script("return window.pageYOffset;")
        scrolling = True
        while scrolling:
            page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
            for card in page_cards[-15:]:
                if card is not None:
                    tweet = get_tweet_data(card)
                    if tweet is not None:
                        tweetL = list(tweet)
                        tweetL.append(x)
                        tweetL.append(j)
                        tweet = tuple(tweetL)
                        if tweet:
                            if tweet[2]<cutoff_date:
                                scrolling=False
                            else:
                                idtweet = list(tweet)
                                idtweet[2]=str(idtweet[2])
                                tweet_id = ''.join(idtweet)
                                if tweet_id not in tweet_ids:
                                    tweet_ids.add(tweet_id)
                                    data.append(tweet)
                    
            scroll_attempt = 0
            while True:
                # check scroll position
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(2)
                curr_position = driver.execute_script("return window.pageYOffset;")
                if last_position == curr_position:
                    scroll_attempt += 1
                    
                    # end of scroll region
                    if scroll_attempt >= 3:
                        scrolling = False
                        break
                    else:
                        sleep(2) # attempt another scroll
                else:
                    last_position = curr_position
                    break
    
        # close the web driver
        driver.close()

