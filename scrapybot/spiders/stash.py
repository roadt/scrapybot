# -*- coding: utf-8 -*-
import sys,os
import re
import scrapy
import logging
import urlparse
from scrapybot.items import *
from scrapybot.spiders import *
from scrapybot.util import *

from scrapy.utils.misc import load_object

logger = logging.getLogger(__name__)



class StashSpider(ArgsSupport, scrapy.Spider):
    '''
     spider for deviantart.com
    '''
    name = "stash"
    allowed_domains = ["sta.sh"]

    def __init__(self, *args, **kwargs):
        super(StashSpider, self).__init__(*args, **kwargs)

    def get(self, name):
        if name in self.kwargs:
            return self.kwargs[name].split(',')
        else:
            return []

    def callback_from_url(self, url):
        """
        determine parse method from url
        """
        if re.search("https?://sta.sh/[^/]+$", url):
            return self.parse_file_page

    def parse_file_page(self, response):
        
        item = File()
        item['url']  = response.url
        item['name'] = response.css('.dev-view-main-content .dev-title-container >  h1 > a::text').extract_first()
        item['author_name'] = response.css('.dev-view-main-content .dev-title-container >  h1 .username::text').extract_first()
        item['author_url'] = response.css('.dev-view-main-content .dev-title-container >  h1 .username::attr("href")').extract_first()

        item['file_url'] = response.css('.dev-view-meta-content  .dev-page-button::attr("href")').extract_first()
        
        for  dt in  response.css('.dev-view-meta-content  .dev-metainfo-details dt'):
            name = dt.xpath('text()').extract_first().strip()
            if name == 'Uploaded on':
                item['date_uploaded'] = dt.xpath('following-sibling::dd/span/@ts').extract_first()
            if name == 'File Size':
                item['file_size'] = dt.xpath('following-sibling::dd/text()').extract_first()

        yield item

