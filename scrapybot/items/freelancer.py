

from scrapy.item import Field, Item


class Job(Item):
    url = Field()

    name = Field()
    description = Field()
    cat_names = Field()

    budget = Field()

    date_started = Field()
    date_end = Field()
    
    bid_count = Field()
    bid_avg = Field()

    
    


    

    
