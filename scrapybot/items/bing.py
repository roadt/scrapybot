# -*- coding: utf-8 -*-

from scrapy.item import Item, Field


class Word(Item):
    url = Field()
    word = Field()
    
    pron_us  = Field()
    pron_us_mp3_url = Field({ 'file_url' : { 'path': 'pron_us_mp3_path'}}) 
    pron_us_mp3_path = Field() 

    pron_uk = Field()
    pron_uk_mp3_url = Field({ 'file_url' : { 'path': 'pron_uk_mp3_path'}}) 
    pron_uk_mp3_path = Field()

    meanings = Field()
    tenses = Field()
    image_urls = Field()

    word_col = Field()
    word_synonym = Field()
    word_antonym = Field()

    detail_auth = Field()
    detail_cross = Field()
    detail_homo = Field()
    detail_web = Field()

    sample_sentences = Field()

