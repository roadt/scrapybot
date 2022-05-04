import logging
import re


import scrapy
from scrapy.selector import *
from scrapy.spiders import *
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapybot.items.qidian import *

logger = logging.getLogger(__name__)


class QidianSpider(Spider):
    '''

    Available arguments
    download urls
    - a url=xxx  -a urls=aaa 

    use a callable to generate urls  (url generator may accept it own args. as following v='xxx')
    -a  urlg=a.b.c.urls_to_down   -a  v=xxx
    
    don't scrap next level
    -a nodeep=True 

    only scrap one page
    -a nonext=True

    '''
    name = 'qidian'
    allowed_domains = ['qidian.com']

    start_urls = ['https://www.qidian.com/all/']

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
        if 'url' in kwargs or 'urls' in kwargs or 'urlg' in kwargs:
            
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

        else:
            for r in super(QidianSpider, self).start_requests():
                yield r



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
        if url.startswith('https://www.qidian.com/all/'):
            return self.parse_article_list
        if re.search('https://book.qidian.com/info/(\d+)/?', url):
            return self.parse_article_detail
        return None

    def parse_article_detail(self, response):
        hxs = response.selector
        i = response.meta.get('article') or  Article()
        i['url'] = response.request.url

        i['title'] = response.css('.book-img img::attr(src)').extract_first().strip()
        i['description'] =  response.css('.book-intro p').extract_first()
        i['cover_url'] = response.css('.book-img img::attr(src)').extract_first()
        return i

    def parse_article_list(self, response):
        hxs = response.selector
        result = []
        for h in hxs.css('.book-img-text ul li'):  #('//div[contains(@class,"sw1") or contains(@class,"sw2")]'):
            i = Article()
            i['title'] = self.extract(h, 'div[@class="book-mid-info"]/h2/a/text()')
            i['url'] = 'https:' + self.extract(h, 'div[@class="book-mid-info"]/h2/a/@href')
            i['description'] = h.css('.book-mid-info .intro::text').extract_first()
            author = h.css('.book-mid-info .author')
            if author:
                i['author_name'] = self.extract(author, 'a[@class="name"]/text()')
                i['author_url'] = 'https:' + self.extract(author, 'a[@class="name"]/@href')
            update = h.css('.book-mid-info .update')
            if update:
                i['char_count'] =  update.css("span > span::text").extract()
                #i['last_update'] = self.extract(h, 'div[@class="swe"]/text()')
            i['key'] = re.search("/(\d+)/?$",i['url']).group(1)
            #Request(i['author_url'],callback=self.parse_user)
            yield i

            # fire to scrap detal page
            if not 'nodeep' in self.kwargs:
                yield Request(i['url'], meta={'article':i},callback=self.parse_article_detail)


        # next gallery page
        if not 'nonext' in self.kwargs:
            next_page = response.xpath('//a[@class="f_a"]/@href').extract_first()
            if next_page:
                url = response.urljoin(next_page)
                req =  scrapy.Request(url, callback=self.parse_article_list)
                yield req


    def parse_user(self, response):
        pass

    def extract(self, hxs, xpath, defv=None):
        arr = hxs.xpath(xpath).extract()
        return arr and arr[0] or defv

