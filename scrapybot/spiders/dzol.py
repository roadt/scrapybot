# -*- coding: utf-8 -*-
import sys,os
import re
import scrapy
import logging
import urlparse
from scrapybot.items.deviantart import *
from scrapybot.spiders import *
from scrapybot.util import *

from scrapy.utils.misc import load_object

logger = logging.getLogger(__name__)


class DzolSpider(ArgSupport, scrapy.Spider):
    ''' detail zol spider '''
    name = "dzol"
    allowed_domains = ["detail.zol.com.cn"]
    start_urls = 'http://detail.zol.com.cn/subcategory.html'

    def __init__(self, *args, **kwargs):
        super(DzolSpider, self).__init__(*args, **kwargs)

    def callback_from_url(self, url):
        """
        determine parse method from url
        """
        if re.search("https?://detail.zol.com.cn/[^/]*/", url) or  re.search("https?://detail.zol.com.cn/[^/]*/subcate[^/]*.html", url):
            return self.parse_subcate_page

        if re.search("https?://detail.zol.com.cn/[^/]*/index[0-9]+.html", url):
            return self.parse_product_index_page


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

