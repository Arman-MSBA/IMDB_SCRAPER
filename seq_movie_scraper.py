# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 18:51:11 2022

@author: arman
"""

from bs4 import BeautifulSoup
from lxml import etree
import requests
import itertools
import pandas as pd
  
URL = "https://www.imdb.com/list/ls003495084/?sort=list_order,asc&st_dt=&mode=detail&page="
  
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})
  

links = []
for p in range(1,13):
    webpage = requests.get(f"{URL}{p}", headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    links.append(dom.xpath('//*[@class="lister-item-index unbold text-primary"]/following::a/@href'))
    print(links)
    
flat_list = list(itertools.chain(*links))


t_ids = []

for i in flat_list:
    if '/title/' in i:
        t_id = i.replace('/?ref_=ttls_li_tt','').replace('/title/','').replace('/?ref_=ttls_li_i','')
        t_ids.append(t_id)
        t_ids = list(set(t_ids))

t_ids = pd.DataFrame(t_ids)

t_ids.to_csv('imdb_sequential_movies.csv')









