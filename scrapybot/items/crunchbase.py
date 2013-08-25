

from scrapy.item import Item, Field


class Company(Item):
    name = Field()
    logo = Field()
    short_description = Field()
    long_description = Field()
    founded_date = Field()
    category = Field()
    # contact
    website = Field()
    blog = Field()
    twitter = Field()
    phone = Field()
    email = Field()
    # mongo item requirement
    key = Field()

class Office(Item):
    name = Field()
    address = Field()
    key = Field()

    company_key = Field()  #belong to which company


class Person(Item):
    name = Field()
    title = Field()
    long_description = Field()

    presence = Field()
    key = Field()
    company_key = Field()
