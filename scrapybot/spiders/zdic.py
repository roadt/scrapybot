# -*- coding: utf-8 -*-
import sys,os
import re
import scrapy
import logging
import urllib.parse
from scrapybot.items.zdic import *
from scrapybot.spiders import *
from scrapybot.util import *

from scrapy.utils.misc import load_object

logger = logging.getLogger(__name__)


class ZDicSpider(ArgsSupport, scrapy.Spider):
    ''' zdic spider '''
    name = "zdic"
    allowed_domains = ["zdic.net"]
    start_urls = ['https://www.zdic.net/zd/bs/']

    hzs_cc1_url = 'http://www.zdic.net/zd/zb/cc1'
    hzs_cc2_url = 'http://www.zdic.net/zd/zb/cc2'
    hzs_ty_url = 'http://www.zdic.net/zd/zb/ty'

    def __init__(self, *args, **kwargs):
        super(ZDicSpider, self).__init__(*args, **kwargs)

    def callback_from_url(self, url):
        """
        determine parse method from url
        """

        #http://www.zdic.net/zd/zb/cc1
        if re.search("https?://www.zdic.net/zd/zb", url):
            return self.parse_z_zb_page

        #http://www.zdic.net/hans/一
        if re.search("https?://www.zdic.net/hans/", url):
            return self.parse_hans_page

        return None

    def parse_hans_page(self, response):
        hz = Hanzi()
        hz['url'] = response.url

        # 基本信息
        #einfo = response.css('#ziif #z_i_1')
        hz['thumb_url'] =  response.urljoin(response.css('#bhbs::attr("src")').extract_first())

        yield hz
        

    def parse_z_js_page(self, response):
        hz = Hanzi()
        hz['url'] = response.url
        
        # 基本信息
        einfo = response.css('#ziif #z_i_1')
        hz['thumb_url'] = "http://www.zdic.net/p/?l=kbg&u=%s&s=100" % re.search("/([^/]*).htm$", response.url).group(1)

        for e in einfo.css('#z_info tr .dicpy'):
            hz['py_name'] = e.css('a::text').extract_first()
            hz['py_url'] = response.urljoin(e.css('a::attr("href")').extract_first())
            hz['audio_url'] = 'http://www.zdic.net/p/mp3/%s.mp3' % re.search('spz\("(.*)"\)', e.css('script::text').extract_first()).group(1) 

            # break, only 1st for now.
            break

        yield hz



    def parse_z_zb_page(self, response):
        for e in response.css('.bs_index3 a'):
            hz = Hanzi()
            hz['url'] = response.urljoin(e.xpath('@href').extract_first())
            hz['name'] = e.xpath('text()').extract_first()
            if self.go('model', 'hanzi', True):
                yield hz
            
            if self.go('rlevel', 'hanzi', False):
                yield scrapy.Request(hz['url'], callback=self.parse_hans_page)
        

    def parse_subcate_page(self, response):
        # basic info
        g = Gallery()
        g['url'] = response.url
        g['name'] = response.css('.folderview .folderview-top .folder-title::text').extract_first()
        g['description'] = response.css('.folderview .folderview-top .description::text').extract_first()
        g['author_url'] = response.css('.catbar a.username::attr("href")').extract_first()
        g['author_name'] = response.css('.catbar .username::text').extract_first()
        g['parent_url'] = response.css('.folderview .folderview-top h1').xpath('a[last()]/@href').extract_first()
        
        if self.go('model', 'gallery', True):
            yield g
        
        # folderview (i.e. arts)
        response.meta['g'] = g
        for e in self.parse_folderview(response):
            yield e
        

        #children galleries
        if self.go('rlevel', 'gchild', True):
            for url in response.css('.gr-box .gr-body .gr  a::attr("href")').extract():
                abs_url = response.urljoin(url)
                if self.callback_from_url(abs_url) == self.parse_gallery_page:
                    r = scrapy.Request(abs_url, callback=self.parse_gallery_page)
                    yield r


