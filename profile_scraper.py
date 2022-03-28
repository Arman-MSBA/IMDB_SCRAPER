#importing libraries
from bs4 import BeautifulSoup
from lxml import etree
import requests
import pandas as pd
import timeit



URL = "https://www.imdb.com/list/ls003495084/?sort=list_order,asc&st_dt=&mode=detail&page="
  
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})
  

url = 'https://www.imdb.com/title/tt0114709/'

data = pd.read_csv("links.csv")
data['links'][1:20]

newdata = []
count = 0

for i in data['links']:
    start = timeit.default_timer()
    webpage = requests.get(i, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    
    diction = {
        'year' : dom.xpath('//span[@class="sc-52284603-2 iTRONr"]')[0].text if bool(dom.xpath('//span[@class="sc-52284603-2 iTRONr"]')) else None,
        'rateing_system' : dom.xpath('//*[@class="sc-52284603-2 iTRONr"]')[1].text if len(dom.xpath('//*[@class="sc-52284603-2 iTRONr"]')) > 1 else None,
        'rating' : dom.xpath('//span[@class="sc-7ab21ed2-1 jGRxWM"]')[0].text if bool(dom.xpath('//span[@class="sc-7ab21ed2-1 jGRxWM"]')) else None,
        'budget' : dom.xpath('.//span[text()="Budget"]//following::span[@class="ipc-metadata-list-item__list-content-item"]')[0].text.replace(' (estimated)','') if bool( dom.xpath('.//span[text()="Budget"]//following::span[@class="ipc-metadata-list-item__list-content-item"]')) else None,
        'op_weekend' : dom.xpath('.//span[text()="Opening weekend US & Canada"]//following::span[@class="ipc-metadata-list-item__list-content-item"]')[0].text if bool(dom.xpath('.//span[text()="Opening weekend US & Canada"]//following::span[@class="ipc-metadata-list-item__list-content-item"]'))  else None,
        'popular' : dom.xpath('//*[@class="sc-edc76a2-1 gopMqI"]')[0].text if bool(dom.xpath('//*[@class="sc-edc76a2-1 gopMqI"]')) else None,
        'director' : dom.xpath('.//span[text()="Director"]//following::a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]')[0].text if bool(dom.xpath('.//span[text()="Director"]//following::a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]')) else None,
        '1st_star' : dom.xpath('.//*[text()="Stars"]//following::a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]')[0].text if len(dom.xpath('.//*[text()="Stars"]//following::a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]')) >= 1 else None,
        '2nd_star' : dom.xpath('.//*[text()="Stars"]//following::a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]')[1].text if len(dom.xpath('.//*[text()="Stars"]//following::a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]')) >= 2  else None,
        '3rd_star' : dom.xpath('.//*[text()="Stars"]//following::a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]')[2].text if len(dom.xpath('.//*[text()="Stars"]//following::a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]')) >= 3 else None,
        'user_review_count' : dom.xpath('//span[@class="score"]')[0].text if bool(dom.xpath('//span[@class="score"]')) else None,
        'critic_review_count' : dom.xpath('//span[@class="score"]')[1].text if len(dom.xpath('//span[@class="score"]')) > 1 else None,
        'meta-score' : dom.xpath('//span[@class="score-meta"]')[0].text if bool(dom.xpath('//span[@class="score-meta"]'))  else None,
        'top_rated' : dom.xpath('//*[@data-testid="award_top-rated"]')[0].text if bool(dom.xpath('//*[@data-testid="award_top-rated"]')) else None,
        'movieid' : i.replace('https://www.imdb.com/title/','').replace('/','')
        }
    
    newdata.append(diction)
    count = count + 1
    
    stop = timeit.default_timer()
    print(f"Time remaining: {((stop - start)*len(data['links'])-count)/60} minutes")
    print(f"Done {count} from {len(data['links'])}")

newdata = pd.json_normalize(newdata,max_level=2)

newdata.to_csv('movie_profile_data.csv')


