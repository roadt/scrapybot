# -*- coding: utf-8 -*-
import sys,os
import re
import scrapy
import logging
import urlparse
import scrapy

from scrapybot.spiders import *
from scrapybot.items.proxylist import *
from scrapybot.util import *


logger = logging.getLogger(__name__)



class ProxylistSpider(ArgsSupport, scrapy.Spider):
    '''
    scrape http://freeproxylists.net/
    '''
    name = "plist"
    allowed_domains = ["freeproxylists.net"]

    start_urls = ['http://freeproxylists.net/']

    def __init__(self, *args, **kwargs):
        super(ProxylistSpider, self).__init__(*args, **kwargs)

    def callback_from_url(self, url):
        return self.parse

    def parse(self, response):
        # extract item
        for sel in response.css('table.DataGrid tr')[1:]:
            # skip ad row 
            if sel.css('ins'):
                continue

            # ok ,extract
            i = iter(sel.css('td'))
            g = Proxy()
            g['ip'] = re.search("[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}", urlparse.unquote(i.next().css('script::text').extract_first())).group()
            g['port'] = i.next().xpath('text()').extract_first()
            g['typ'] = i.next().xpath('text()').extract_first()
            g['anonymity'] = i.next().xpath('text()').extract_first()
            g['country'] = i.next().xpath('text()').extract_first()
            g['region'] = i.next().xpath('text()').extract_first()
            g['city'] = i.next().xpath('text()').extract_first()
            g['uptime'] = float(i.next().xpath('text()').extract_first().rstrip('%'))
            g['response'] = int(re.search("width:(.*)%", i.next().css('span::attr("style")').extract_first()).group(1))
            g['transfer'] =  int(re.search("width:(.*)%", i.next().css('span::attr("style")').extract_first()).group(1))

            #key
            g['key'] = g['ip']
            yield g

        #next page
        if self.go('next', 'plist', True):
            url = response.css('.page').xpath('a[contains(text(),"Next")]/@href').extract_first()
            yield scrapy.Request(response.urljoin(url), callback=self.parse)


            
        