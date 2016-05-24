# -*- coding: utf-8 -*-
import sys,os
import re
import scrapy
import logging
import urlparse
from scrapybot.items.pptv import *
from scrapybot.spiders import *
from scrapybot.util import *

from scrapy.utils.misc import load_object

logger = logging.getLogger(__name__)



class CacheSpider(ArgsSupport, scrapy.Spider):
    '''
    cahce spider -  simple spider   rather than scrap  items ,  only navigate all possible urls. 
    use with http enabled to help http cache component to get page caches.  it has filter support to filter out url you need by scheme, url regex, or
    any logic filter you extend  by including it in  'urlf='.

    -a urlf=callable1,callbale2  -    any one return true, url is passed (scheme, regex is in list by default, which read  regex=, scheme= and check)
    -a regex=regex1,regex2  -     any one return true, url is passed
    -a scheme=http,ftp  - etc..      
    -a domain=domain1,domain2 -  set allowed_domains of spider - used by offsite middle

    with  little modification, it can return Url Item to become a general & powerful web spider.
    '''
    name = "cache"

    def __init__(self, *args, **kwargs):
        super(CacheSpider, self).__init__(*args, **kwargs)
        if 'domain' in kwargs:
            self.allowed_domains =  kwargs['domain'].split(',')
        if 'scheme' in kwargs:
            self.schemes = kwargs['scheme'].split(',')
        else:
            self.schemes = ['http', 'https']

    def get(self, name):
        if name in self.kwargs:
            return self.kwargs[name].split(',')
        else:
            return []

    def callback_from_url(self, url):
        """
        determine parse method from url
        """
        return self.parse


    def parse(self, response):

        # 1st, if the response is not text/html, pass, httpcache will cache it anway
        if not re.search("text/html", response.headers['Content-Type']):
            logger.info("%s:%s %s" % (type(self).__name__,  'parse - can not parse',  [response.url, response.headers]))
            
        
        # others (images, stylesheets, scripts)
        # no filter check need, it is mostly needed for cache a site
        # give each have a global  swtich to skip
        cfg = {
            'image' : 'img::attr("src")',
            'stylesheet' : 'link[rel="stylesheet"]::attr("href")',
            'script'  : 'script::attr("src")'
        }
        for cat, expr in cfg.iteritems():
            if self.go('rlevel', cat, True):
                for url in response.css(expr).extract():
                    abs_url = response.urljoin(url)
                    logger.debug("%s:%s %s" % (type(self).__name__,  'parse - %s' % cat,  [abs_url]))
                    yield scrapy.Request(abs_url, callback=self.parse_none)
        
        #links - <a>
        for url in response.css('a::attr("href")').extract():
            abs_url = response.urljoin(url)
            # do fliter check
            if self.urlfilter_passed(abs_url):
                logger.info("%s:%s %s" % (type(self).__name__,  'parse - pass - url ',  [abs_url]))
                yield scrapy.Request(abs_url, callback=self.parse)


    def parse_none(self, response):
        pass


    def urlfilter_passed(self, url):
        '''  check url from urlf fliter ("urlf=filter1,fitler2")
        url pass if fitler1, fitler2 all return true for it
        
        two filter is default in filter list.  scheme, regex
        scheme check  url's scheme  (scheme=http,ftp)
        regex check url to a regular expressioin (regex=regex1,regex2   regex1,regex2 is OR relationship)
        '''
        # collect filter
        urlf_names = self.get('urlf')
        # support 'regex='
        default_urlfs = ['scrapybot.urlf.scheme', 'scrapybot.urlf.regex']
        for f in default_urlfs:
            if not f in urlf_names:
                urlf_names.insert(0,f)

        kwargs  = {k: v for k,v in self.kwargs.iteritems() if k != 'url'}
        #  any  one deny, deny
        ok = True
        for urlf in urlf_names:
            try: 
                f = load_object(urlf)
                if callable(f):
                    ok = f(url, **kwargs)
            except Exception as e: 
                logger.error("%s:%s %s" % (type(self).__name__,  'urlfilter_passed',  [self.kwargs, url, ok, e, sys.gettrace()]))

            if not ok:  # one deny
                break

        return ok




            
        