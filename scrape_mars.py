###!/usr/bin/env python3

import os
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "c:/bin/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_data = {}


##############################################################################
    # NASA Mars News - Challenge
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)
    soup = bs(browser.html, 'html.parser')
    #title = soup.title.text
    #print(title)

    newest_link = soup.find('div', class_="list_text")
    newest_link_title = newest_link.find('div', class_="content_title").text
    print(newest_link_title)
    mars_data["newest_link_title"] = newest_link_title

    newest_link_body = newest_link.find('div', class_="article_teaser_body").text
    print(newest_link_body)
    mars_data["newest_link_body"] = newest_link_body


##############################################################################
    # JPL Mars Space Images - Featured Image - Challenge
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)
    soup = bs(browser.html, 'html.parser')

    # Click the 'FULL IMAGE' button on the page
    try:
        # Deprecated
        # browser.click_link_by_partial_text("FULL IMAGE")
        
        # Also Deprecated
        # browser.find_link_by_partial_text("FULL IMAGE")
        
        button = browser.links.find_by_partial_text("FULL IMAGE")
        button.click()
        
    except:
        print("Cannot find FULL IMAGE button to click!")

    time.sleep(1)
    soup = bs(browser.html, 'html.parser')
    temp = soup.find("div", class_="fancybox-inner")
    #temp = soup.find("img", class_="fancybox-image")

    #print(temp.prettify())
    path = temp.find("img").get("src")

    featured_image_url = "https://www.jpl.nasa.gov" + path
    print(featured_image_url)
    mars_data["featured_image_url"] = featured_image_url


##############################################################################
    # Mars Facts - Challenge
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(2)
    soup = bs(browser.html, 'html.parser')

    mars_facts_df = pd.read_html('https://space-facts.com/mars/')[0]
    #mars_facts_df

    mars_facts_df.rename(columns={0: "Name", 1: "Value"}, inplace=True)
    #mars_facts_df

    mars_facts_html_table = mars_facts_df.to_html
    mars_facts_html_table_code = mars_facts_df.to_html(index=False)
    print(mars_facts_html_table)
    mars_data["mars_facts_html_table_code"] = mars_facts_html_table_code


##############################################################################
    # Mars Hemispheres - Challenge

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(2)
    soup = bs(browser.html, 'html.parser')

    # 8 items
    #hemisphere_a = soup.find_all("a", class_="itemLink")

    # 4 items
    hemisphere_links = soup.find_all("div", class_="item")

    # Process the anchor tags to get the hrefs and store in a list
    my_list = []

    for i in range(len(hemisphere_links)):
        
        #print(hemisphere_links[i].find("a"))
        
        href = hemisphere_links[i].find("a").get("href")
        title = hemisphere_links[i].find("h3").text
        url = "https://astrogeology.usgs.gov" + href
        print(title)
        print(url)
        
        browser.visit(url)
        time.sleep(1)
        soup = bs(browser.html, 'html.parser')
        
        # I'm grabbing the sample image instead of the full image because the full image is 21 MB!!
        sample_img_url = soup.find('a', href=True, text='Sample').get("href")
        print(sample_img_url)
        img_url = soup.find('a', href=True, text='Original').get("href")
        print(img_url)
        
        data = {}
        data["title"] = title
        data["sample_img_url"] = sample_img_url
        data["img_url"] = img_url
        #print(data)
        
        my_list.append(data)
    # End of For Loop

    mars_data["hemisphere_data"] = my_list

    browser.quit()

    return mars_data
    

# print("Hello There!")
# scrape()
# print("Another happy landing!")


