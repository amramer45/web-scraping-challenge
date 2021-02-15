#!/usr/bin/env python
# coding: utf-8

#Import dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time

def init_browser(): 
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():

    mars_dict={}

    ####### Mars News #########
    try: 
        #URL information of the page to be scraped
        url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
        browser.visit(url)
        time.sleep(3)
        html=browser.html
        soup=bs(html, 'html.parser')

        #Retrieve latest news title and paragraph text (use variables for reference later)
        results=soup.find('li', class_='slide')

        news_title = results.find('div', class_='content_title').text
        news_p = results.find('div', class_='article_teaser_body').text

        mars_dict["news_title"]=news_title
        mars_dict["news_p"]=news_p

        print("space news success")
    except:
        mars_dict['news_title']= '1news_title'
        mars_dict["news_p"]='2news_p'
        print('mars new failure')

    ####### Featured Image ########
    try:
        image_url='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
        browser.visit(image_url)

        html=browser.html
        soup=bs(html, 'html.parser')

        image_tag=soup.find('img', class_='headerimage')
        partial_url=image_tag.get('src')
        featured_image_url=(f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{partial_url}')

        mars_dict["featured_image_url"]=featured_image_url
        print("featured image success")
    except:
        mars_dict["featured_image_url"]='1featured_image'
        print('featured image failure')



    ####### Mars Facts #########

    try:
        #Scrape Mars facts
        facts_url='https://space-facts.com/mars/'
        mars_facts_df=pd.read_html(facts_url)[0]

        mars_facts_df.columns=['Characteristics', 'Mars']
        mars_facts_df.set_index('Characteristics', inplace=True)

        mars_table_html=mars_facts_df.to_html(index=True, header=True, border=0, justify="left")

        mars_dict["mars_facts"]=mars_facts_df
        print("mars facts success")
    except:
       mars_dict["mars_facts"]='1mars_facts'
       print('facts failure')


    ######### Mars Hemispheres #########

    try:
        #Scrape Mars hemisphere title and image
        usgs_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(usgs_url)

        html=browser.html
        soup=bs(html, 'html.parser')


        hem_list=[]
        count=0
        mars_hemi_url='https://astrogeology.usgs.gov/'
        hemisphere_locate=soup.find_all('div', class_='item')

        for results in hemisphere_locate:
            mars_title=results.find('h3').text
            browser.links.find_by_partial_text(mars_title).click()
            time.sleep(1)

            html=browser.html
            soup=bs(html, 'html.parser')
            partial_image=soup.find('img', class_='wide-image')['src']

            img_url=mars_hemi_url+partial_image

            #Create list of dictionaries
            hem_list.append({
                'title':mars_title,
                'img_url':img_url
            })

            count=count+1
            
            if len(hemisphere_locate)>count:
                browser.back()
                time.sleep(1)
            else:
                break

        mars_dict["hem_list"]=hem_list
        print('mars hemisphere success')
    except:
        mars_dict["hem_list"]='hemisphere_info'
        print('hemisphere failure')

    browser.quit()
    print('Quitting Browser')

    print('Scrapping Complete')
    return mars_dict