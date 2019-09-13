# -*- coding: utf-8 -*-

from scrapy.item import Item, Field

class Hanzi(Item):
    '''http://www.zdic.net/z/15/js/4E2D.htm'''
    url = Field()

    name = Field()
    thumb_url = Field({  'file_url' : { 'path': 'thumb_path'}}) 
    thumb_path = Field()

    # pinyin/zhuyin 注音
    py_name = Field()
    py_url = Field()
    audio_url = Field()
    #audio_url = Field({'file_url' : { 'path': 'audio_path'}})
    audio_path = Field()

    zy = Field()



    # 部首
    jbs = Field()
    jbh = Field()
    jzbh = Field()
    fbs = Field()


    #input-method
    im_unicode = Field()
    im_wubi = Field()
    im_changjie = Field()
    im_zhengma = Field()
    im_sijiao = Field()
    im_bishun = Field()
    
    _headers = None

class Pinyin(Item):
    '''http://www.zdic.net/z/pyjs/?py=zhong1'''
    url = Field()
    name = Field()

    mp3_url = Field({ 'mp3_url' : {'path': 'mp3_path'}})
    mp3_path = Field()



class HanziSet(Item):
    ''' http://www.zdic.net/z/zb/cc1.htm '''
    name = Field()
    url = Field()
    hanzi = Field()


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