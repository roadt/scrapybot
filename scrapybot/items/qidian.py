

#
#  put  Qidan site's aritcle  items definition
#
#
from scrapy.item import Item, Field

class Article(Item):
    title = Field()
    url = Field()
    author_name = Field()
    author_url = Field()
    char_count = Field()
    last_update = Field()
    key = Field()
