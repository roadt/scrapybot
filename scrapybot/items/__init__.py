
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ScrapybotItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass




class File(Item):
    
    url = Field()

    name = Field()
    file_url = Field({'file_url': {'path': 'file_path', 'cb': 'file_path_cb'}}) 
    file_path = Field()
    file_size = Field()

    date_uploaded = Field()
    
    author_name = Field()
    author_url = Field()

    def file_path_cb(self, url):
        '''http://sta.sh/download/5979801669005771/tda_saber_lily_ver_1_00_silver_by_samsink_by_samsink-d9mpyaj.rar?token=edfaad9bce33e69936d776cbf36646bdcf6a445e&ts=1471602742  ->  sta.sh/download/5979801669005771/tda_saber_lily_ver_1_00_silver_by_samsink_by_samsink-d9mpyaj.rar'''
        url = url.split('?')[0]
        return '/'.join(url.split('/')[2:])