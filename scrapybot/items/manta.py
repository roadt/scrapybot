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


