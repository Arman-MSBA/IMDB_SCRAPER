# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:21:51 2022

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
  

url = 'https://www.imdb.com/title/tt0114709/parentalguide'

data = pd.read_csv("C:/Users/arman/OneDrive/Desktop/links.csv")
data["parentguide_links"][1:20]

newdata = []
count = 0

for i in data["parentguide_links"]:
    start = timeit.default_timer()
    webpage = requests.get(i, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    
    diction = {
        'sex_&_nudity' : dom.xpath('.//*[@id="ipl-swapper__control-nudity"]//following::a[@class="advisory-severity-vote__message"]')[0].text.split()[-1] if bool(dom.xpath('.//*[@id="ipl-swapper__control-nudity"]//following::a[@class="advisory-severity-vote__message"]')) else None,
        'Violence_&_Gore' : dom.xpath('.//*[@id="ipl-swapper__control-violence"]//following::a[@class="advisory-severity-vote__message"]')[0].text.split()[-1] if bool(dom.xpath('.//*[@id="ipl-swapper__control-violence"]//following::a[@class="advisory-severity-vote__message"]')) else None,
        'profanity' : dom.xpath('.//*[@id="ipl-swapper__control-profanity"]//following::a[@class="advisory-severity-vote__message"]')[0].text.split()[-1] if bool(dom.xpath('.//*[@id="ipl-swapper__control-profanity"]//following::a[@class="advisory-severity-vote__message"]')) else None,
        'alcohol' : dom.xpath('.//*[@id="ipl-swapper__control-alcohol"]//following::a[@class="advisory-severity-vote__message"]')[0].text.split()[-1] if bool(dom.xpath('.//*[@id="ipl-swapper__control-alcohol"]//following::a[@class="advisory-severity-vote__message"]')) else None,
        'frightening' : dom.xpath('.//*[@id="ipl-swapper__control-frightening"]//following::a[@class="advisory-severity-vote__message"]')[0].text.split()[-1] if bool(dom.xpath('.//*[@id="ipl-swapper__control-frightening"]//following::a[@class="advisory-severity-vote__message"]')) else None,
        'movieid' : i.replace('https://www.imdb.com/title/','').replace('/parentalguide','')
        }
    
    newdata.append(diction)
    count = count + 1
    
    stop = timeit.default_timer()
    print(f"Time remaining: {((stop - start)*len(data['links'])-count)/60} minutes")
    print(f"Done {count} from {len(data['links'])}")

newdata = pd.json_normalize(newdata,max_level=2)

newdata.to_csv('movie_parentguide_data.csv')




