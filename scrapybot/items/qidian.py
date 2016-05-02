

#
#  put  Qidan site's aritcle  items definition
#
#
from scrapy.item import Item, Field

class Article(Item):

    url = Field()  # url of target site

    # data fields
    title = Field()
    cover_url = Field({ 'file_url': { 'path': 'cover_path'}})
    cover_path = Field()

    author_name = Field()
    author_url = Field()
    char_count = Field()
    last_update = Field()
    key = Field()

    description = Field()
