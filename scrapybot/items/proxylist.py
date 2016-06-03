


from scrapy.item import Item, Field


class Proxy(Item):
    ''' info of  proxy server'''
    ip  = Field()
    port = Field()
    
    typ = Field()

    anonymity = Field()
    country = Field()
    region = Field()
    city = Field()
    uptime = Field()
    
    response = Field()
    transfer = Field()

    key = Field()

