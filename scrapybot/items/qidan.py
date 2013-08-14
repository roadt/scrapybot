

#
#  put  Qidan site's aritcle  items definition 
# 
#
from scrapy.item import Item, Field


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
