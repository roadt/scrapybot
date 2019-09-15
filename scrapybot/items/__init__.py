
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
import re

class ScrapybotItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass




class File(Item):
    
    url = Field()

    name = Field()
    #file_url = Field()
    file_url = Field({'file_url': {'path': 'file_path', 'cb': 'file_path_cb'}}) 
    file_path = Field()
    file_size = Field()
    file_ext = Field()

    date_uploaded = Field()
    
    author_name = Field()
    author_url = Field()

    _headers = None

    def file_path_cb(self, url, item=None):
        '''
http://sta.sh/download/5979801669005771/tda_saber_lily_ver_1_00_silver_by_samsink_by_samsink-d9mpyaj.rar?token=edfaad9bce33e69936d776cbf36646bdcf6a445e&ts=1471602742  ->  sta.sh/download/5979801669005771/tda_saber_lily_ver_1_00_silver_by_samsink_by_samsink-d9mpyaj.rar

https://sta.sh/download/5984500926016831/dad5k04-938f830d-6763-42b4-930a-d2de449ab736?token=f37302aef0a11adf7eae92b910618c2a9f190d17&ts=1568536014
        '''
        url = url.split('?')[0]
        file_path =   '/'.join(url.split('/')[2:]) 
        return file_path + '.' + item.get('file_ext')

