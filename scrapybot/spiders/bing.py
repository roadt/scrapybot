# -*- coding: utf-8 -*-
import sys,os
import re
import scrapy
import logging
import urllib.parse
from scrapybot.items.bing import *
from scrapybot.spiders import *
from scrapybot.util import *

from scrapy.utils.misc import load_object

logger = logging.getLogger(__name__)



class BingSpider(ArgsSupport, scrapy.Spider):
    name = 'bing'
    allowed_domains = ['bing.com']
    start_urls = ['https://bing.com/']

    def parse(self, response):
        pass


class BingDictSpider(ArgsSupport, scrapy.Spider):
    name = 'bing.dict'
    allowed_domains = ['bing.com']
    start_urls = ['https://cn.bing.com/dict']

    def callback_from_url(self, url):
        if re.search("https?://cn.bing.com/dict/search.*", url):
            return self.parse_search_page


    def parse(self, response):
        return self.parse_search_page(response)

    def parse_search_page(self, response):
        rs = response.selector
        qdef = rs.css(".qdef")

        i = Word()

        # url, word
        i['word'] = word = qdef.css('#headword strong::text').extract_first()
        i['url'] = "https://cn.bing.com/dict/search?q=" + word

        # pronounces
        hd_prUS = qdef.css('.hd_area .hd_prUS')
        i['pron_us']  = hd_prUS.xpath('text()').extract_first()
        i['pron_us_mp3_url'] = hd_prUS.xpath('following-sibling::*[1]').css('.bigaud::attr(onmouseover)').re_first('https://.*.mp3')

        hd_pr = qdef.css('.hd_area .hd_pr')
        i['pron_uk']  = hd_pr.xpath('text()').extract_first()
        i['pron_uk_mp3_url'] = hd_pr.xpath('following-sibling::*[1]').css('.bigaud::attr(onmouseover)').re_first('https://.*.mp3')

        # meanings
        i['meanings'] = qdef.css('ul').extract()
        i['tenses'] = qdef.css('.hd_div1 div').extract_first()
        i['image_urls'] = qdef.css('.img_area .simg img::attr(src)').extract()

        # related
        i['word_synonym'] = qdef.css('#synoid .df_div2').extract_first()
        i['word_antonym'] = qdef.css('#antoid .df_div2').extract_first()

        # detail eamnings
        df = qdef.css('#defid')
        i['detail_auth'] = qdef.css('#authid .each_seg').extract_first()
        i['detail_cross'] = qdef.css('#crossid .each_seg').extract_first()
        i['detail_homo'] = qdef.css('#homoid .each_seg').extract_first()
        i['detail_web'] = qdef.css('#webid .each_seg').extract_first()

        # sample sentences
        i['sample_sentences'] = rs.css('#sentenceSeg .se_li').extract()
        yield i
