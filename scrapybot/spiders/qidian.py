import logging
import re


import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapybot.items.qidian import *

logger = logging.getLogger(__name__)


class QidianSpider(BaseSpider):
    name = 'qidian'
    allowed_domains = ['qidian.com']

    start_urls = ['http://all.qidian.com/book/bookstore.aspx']

    def __init__(self, *args, **kwargs):
        super(QidianSpider, self).__init__(*args, **kwargs)
        self.kwargs = kwargs

    def parse(self, response):
        """
        reserved for  "scrapy parse"
        """

        url = response.request.url
        callback = self.callback_from_url(url)
        return callback(response)


    def start_requests(self):
        kwargs = self.kwargs

        #if kwags is emtpy, route to old logic
        if not kwargs:
            return super(QidianSpider, self).start_requests(*args, **kwargs)
            
        # setup urls , and parse kwargs
        urls = set()
        
        # deal with url, urls param
        param_url = kwargs.get('url')
        param_urls = kwargs.get('urls')
        param_urls = param_urls and param_urls.split(',') 
        if param_url:
             urls.add(param_url)
        if param_urls:
            urls = urls.union(param_urls)

    
        # deeal wiht urlgen
        param_urlg = kwargs.get('urlg')
        if param_urlg:
            urlg = load_object(param_urlg)
            if callable(urlg):
                urls = urls.union(urlg(**kwargs))

        logger.debug("%s:%s %s" % (type(self).__name__,  'start_requests',  [kwargs, urls]))
        for url in urls:
            callback = self.callback_from_url(url)
            if callback:
                yield scrapy.Request(url, callback=callback)


    def urls_from_generator(self, urlg, **kwargs):
        urls = []
        try: 
            urlg = load_object(param_urlg)
            if callable(urlg):
                urls = urlg(**kwargs)
        except: 
            logger.error("%s:%s %s" % (type(self).__name__,  'urls_from_generator',  [kwargs, urlg, urls]))

        return urls
        

    def make_requests_from_url(self, url):
        callback = self.callback_from_url(url)
        if callback:
            return scrapy.Request(url, callback=callback)
        return None

    def callback_from_url(self, url):
        if url.startswith('http://all.qidian.com/'):
            return self.parse_article_list
        if re.search('http://www.qidian.com/Book/(\d+).aspx', url):
            return self.parse_article_detail
        return None

    def parse_article_detail(self, response):
        hxs = HtmlXPathSelector(response)
        i = response.meta.get('article') or  Article()
        i['url'] = response.request.url

        i['title'] = response.xpath('//div[@class="book_info"]/descendant::*[@itemprop="name"]/child::text()').extract_first().strip()
        i['description'] =  response.xpath('//div[@class="book_info"]/descendant::*[@itemprop="name"]/child::text()').extract_first().strip()
        i['cover_url'] = response.xpath('//div[@class="pic_box"]/a/img[@itemprop="image"]/@src').extract_first()
        i['description'] = self.extract(hxs, '//span[@itemprop="description"]/text()').strip()
        #print i['description']
        return i

    def parse_article_list(self, response):
        hxs = HtmlXPathSelector(response)
        result = []
        for h in hxs.select('//div[contains(@class,"sw1") or contains(@class,"sw2")]'):
            i = Article()
            i['title'] = self.extract(h, 'div[@class="swb"]/span/a/text()')
            i['url'] = self.extract(h, 'div[@class="swb"]/span/a/@href')
            i['author_name'] = self.extract(h, 'div[@class="swd"]/a/text()')
            i['author_url'] = self.extract(h, 'div[@class="swd"]/a/@href')
            i['char_count'] = self.extract(h, 'div[@class="swc"]/text()', 0)
            i['last_update'] = self.extract(h, 'div[@class="swe"]/text()')
            i['key'] = re.search("/(\d+).aspx$",i['url']).group(1)
            #Request(i['author_url'],callback=self.parse_user)
            yield Request(i['url'], meta={'article':i},callback=self.parse_article_detail)


    def parse_user(self, response):
        pass

    def extract(self, hxs, xpath, defv=None):
        arr = hxs.select(xpath).extract()
        return arr and arr[0] or defv
