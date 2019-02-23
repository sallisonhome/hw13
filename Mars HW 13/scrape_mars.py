import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from selenium import webdriver
import requests as req
import re

from splinter import browser
from selenium import webdriver



def scrape():
#scrape the NASA Mars News SIte, collect news title, paragraph text, assign
#to variables for later reference
    url = "https://mars.nasa.gov/news/" 
    response = req.get(url)
    soup = bs(response.text, 'html5lib')

#Scrape for news item
    news_title = soup.find("div", class_="content_title").text
    paragraph_text = soup.find("div", class_="rollover_description_inner").text




# JPL's Space images

    executable_path = {'executable_path' : 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

#call soup 
    html = browser.html
    soup = bs(html, "html.parser")

#auto click through to full image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')

#soup gets image url
    new_html = browser.html
    new_soup = bs(new_html, 'html.parser')
    temp_img_url = new_soup.find('img', class_='main_image')
    recent_mars_image_url = "https://www.imagecache.jpl.nasa.gov/images/640x350/PIA18605-16-640x350.jpg"

#getdata from Twitter for Mars Weather
    twitter_req = req.get("https://twitter.com/marswxreport?lang=en")
    twitter_bs = bs(twitter_req.text, 'html.parser')

    tweet_output = twitter_bs.find_all('div', class_="js-tweet-text-container")

    for i in range(10):
        tweets = tweet_output[i].text
        if "Sol " in tweets:
            mars_weather=tweets
            break

#MARS FACTS. 
    request_mars_facts = req.get("https://space-facts.com/mars/")

    mars_table = pd.read_html(request_mars_facts.text)
    mars_df = mars_table[0]

    mars_df.set_index(0, inplace=True)
    mars_df2 =mars_df

    mars_data_html = mars_df2.to_html()
    mars_data_html.replace('\n', '')
    mars_df2.to_html('mars_table.html')

#Get pics of Mars' hemispheres
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    usgs_req = req.get(usgs_url)


    soup = bs(usgs_req.text, "html.parser")
    hemis_list = soup.find_all('a', class_="itemLink product-item")


    hemisphere_image_urls = []
    for hemi_img in hemis_list:
        img_title = hemi_img.find('h3').text
        link_to_img = "https://astrogeology.usgs.gov/" + hemi_img['href']
        img_request = req.get(link_to_img)
        soup = bs(img_request.text, 'lxml')
        img_tag = soup.find('div', class_='downloads')
        img_url = img_tag.find('a')['href']
        hemisphere_image_urls.append({"Title": img_title, "Image_Url": img_url})

    mars_data = {
        "News_Title": news_title,
        "Paragraph_Text": paragraph_text,
        "Most_Recent_Mars_Image": recent_mars_image_url,
        "Mars_Weather": mars_weather,
        "mars_h": hemisphere_image_urls
        }

    return mars_data
