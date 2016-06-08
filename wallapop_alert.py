#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import demiurge, os, pickle, tempfile

urlSearch = 'http://es.wallapop.com/search?kws=gameboy&maxPrice=&dist=0_&order=creationData-des&kws=sp+101&lat=41.398077&lng=2.170432'
urlWallapop = 'http://es.wallapop.com'
SAVE_LOCATION = os.path.join(tempfile.gettempdir(), 'alertWallapop.pkl')
data_save = False

# Demiurge for get products in Wallapop
class Products(demiurge.Item):
    title = demiurge.TextField(selector='a.product-info-title')
    price = demiurge.TextField(selector='span.product-info-price')
    url = demiurge.AttributeValueField(selector='div.card-product-product-info a.product-info-title', attr='href')

    class Meta:
        selector = 'div.card-product'

        
def sendPushBullet(title, body, url):
    command = "curl -X POST -H 'Access-Token: <You Token>' -F 'email={email}' -F 'type=link' -F 'title={title}' -F 'body={body}' -F 'url={url}' 'https://api.pushbullet.com/v2/pushes'".format(email='<You email>', title=title, body=body, url=url)
    os.system(command)



# Load after data search
try:
    dataFile = open(SAVE_LOCATION, 'rb')
    data_save = pickle.load(dataFile)
except:
    pass

# Read web
results = Products.all(urlSearch)
data_temp = []

for item in results:
    data_temp.append({'title': item.title
                      , 'price': item.price
                      , 'url': urlWallapop + item.url })

# Check new items
list_news = []
if data_save != data_temp: 
    for item in data_temp:
        if item not in data_save:
            list_news.append(item)

# Send alert
for item in list_news:
    sendPushBullet('Wallapop: ' + item['title'], item['price'], item['url'])

# Save data
data_save = open(SAVE_LOCATION, 'wb')
pickle.dump(data_temp, data_save)
