# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:56:21 2022

@author: arman
"""

#importing libraries
from bs4 import BeautifulSoup
from lxml import etree
import requests
import pandas as pd
import timeit

  
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})
  

url = 'https://www.imdb.com/title/tt0114709/ratings'

data = pd.read_csv("C:/Users/arman/OneDrive/Desktop/links.csv")
data["ratings"][0]
 
newdata = []
count = 0

for i in data["ratings"]:
    start = timeit.default_timer()
    webpage = requests.get(i, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    
    diction = {
        'all_all_ages': dom.xpath('.//*[text()="All"]//following::div[@class="bigcell"]')[0].text if bool(dom.xpath('.//*[text()="All"]//following::div[@class="bigcell"]')) else None,
        'all_<18':  dom.xpath('.//*[text()="All"]//following::div[@class="bigcell"]')[1].text if len(dom.xpath('.//*[text()="All"]//following::div[@class="bigcell"]')) >1 else None,
        'all_18-29':  dom.xpath('.//*[text()="All"]//following::div[@class="bigcell"]')[2].text if len(dom.xpath('.//*[text()="All"]//following::div[@class="bigcell"]')) >2 else None,
        'all_30-44':  dom.xpath('.//*[text()="All"]//following::div[@class="bigcell"]')[3].text if len(dom.xpath('.//*[text()="All"]//following::div[@class="bigcell"]')) >3 else None,
        'all_45+':  dom.xpath('.//*[text()="All"]//following::div[@class="bigcell"]')[4].text if len(dom.xpath('.//*[text()="All"]//following::div[@class="bigcell"]')) >4 else None,
        'males_all_ages': dom.xpath('.//*[text()="Males"]//following::div[@class="bigcell"]')[0].text if bool(dom.xpath('.//*[text()="Males"]//following::div[@class="bigcell"]')) else None,
        'males_<18':  dom.xpath('.//*[text()="Males"]//following::div[@class="bigcell"]')[1].text if len(dom.xpath('.//*[text()="Males"]//following::div[@class="bigcell"]')) >1 else None,
        'males_18-29':  dom.xpath('.//*[text()="Males"]//following::div[@class="bigcell"]')[2].text if len(dom.xpath('.//*[text()="Males"]//following::div[@class="bigcell"]')) >2 else None,
        'males_30-44':  dom.xpath('.//*[text()="Males"]//following::div[@class="bigcell"]')[3].text if len(dom.xpath('.//*[text()="Males"]//following::div[@class="bigcell"]')) >3 else None,
        'males_45+':  dom.xpath('.//*[text()="Males"]//following::div[@class="bigcell"]')[4].text if len(dom.xpath('.//*[text()="Males"]//following::div[@class="bigcell"]')) >4 else None,
        'females_all_ages': dom.xpath('.//*[text()="Females"]//following::div[@class="bigcell"]')[0].text if bool(dom.xpath('.//*[text()="Females"]//following::div[@class="bigcell"]')) else None,
        'females_<18':  dom.xpath('.//*[text()="Females"]//following::div[@class="bigcell"]')[1].text if len(dom.xpath('.//*[text()="Females"]//following::div[@class="bigcell"]')) >1 else None,
        'females_18-29':  dom.xpath('.//*[text()="Females"]//following::div[@class="bigcell"]')[2].text if len(dom.xpath('.//*[text()="Females"]//following::div[@class="bigcell"]')) >2 else None,
        'females_30-44':  dom.xpath('.//*[text()="Females"]//following::div[@class="bigcell"]')[3].text if len(dom.xpath('.//*[text()="Females"]//following::div[@class="bigcell"]')) >3 else None,
        'females_45+':  dom.xpath('.//*[text()="Females"]//following::div[@class="bigcell"]')[4].text if len(dom.xpath('.//*[text()="Females"]//following::div[@class="bigcell"]')) >4 else None,
        'movieid' : i.replace('https://www.imdb.com/title/','').replace('/ratings','')
        }
    
    newdata.append(diction)
    count = count + 1
    
    stop = timeit.default_timer()
    print(f"Time remaining: {((stop - start)*len(data['links'])-count)/60} minutes")
    print(f"Done {count} from {len(data['links'])}")

newdata = pd.json_normalize(newdata,max_level=2)

newdata.to_csv('movie_demographic_data.csv')






