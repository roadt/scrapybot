# -*- coding: utf-8 -*-

from scrapy.item import Item, Field


class Anim(Item):

    url = Field()

    thumb_url = Field({ 'file_url' : { 'path': 'thumb_path'}})
    thumb_path = Field()
    cover_url = Field({ 'file_url' : { 'path': 'cover_path'}})
    cover_path = Field()
    
    name = Field()
    description = Field()
    name_alias = Field()
    actor_names  = Field()
    director_names = Field()
    area_name = Field()
    category_names = Field()
    date_publish = Field()
    duration = Field()
    quality = Field()  # 2 - 超清, 3 - 蓝光


    #
    tag_names = Field()
    rate_avg = Field()
    video_count = Field()
    completed = Field()   # 完结
    play_count = Field()
    play_url = Field()
    play_urls = Field()
    


class Actor(Item):
    url = Field()