# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ScrapybotItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass


class Company(Item):
    name = Field()
    manta_url = Field()
    street = Field()
    locality = Field()
    region = Field()
    postal_code = Field()
    phone = Field()
    website = Field()



class Article(Item):
    title = Field()
    url = Field()
    author_name = Field()
    author_url = Field()
    char_count = Field()
    last_update = Field()
