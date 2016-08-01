# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import logging
from scrapy.utils.misc import load_object
logger = logging.getLogger(__name__)


class ArgsSupport(object):
    '''
    argument support mixins

    '''
    def __init__(self, *args, **kwargs):
        super(ArgsSupport, self).__init__(*args, **kwargs)
        self.kwargs =self.parse_kwargs(kwargs)


    def parse_kwargs(self, kwargs):
        for key in ['url', 'urlg', 'rlevel', 'next']:
            if key in kwargs:
                if isinstance(kwargs[key], list):
                    kwargs[key] = kwargs[key]
                else:
                    kwargs[key] = kwargs[key].split(',')
            # request level  (rlevel=page, means will request page url & parse)
            # next page
        return kwargs

    def parse(self, response):
        """
        reserved for  "scrapy parse"
        """

        url = response.request.url
        callback = self.callback_from_url(url)
        return callback(response)


    def start_requests(self):
        kwargs = self.kwargs

        # ugl generator,  the generator will update the kwargs in the end.
        param_urlgs = kwargs.get('urlg')
        if param_urlgs:
            for urlg in param_urlgs:
                urlg = load_object(urlg)
                if callable(urlg):
                    kwargs.update(urlg(**kwargs))

        # urls
        urls = set()
        param_url = kwargs.get('url')
        if param_url:
            urls = urls.union(param_url)

        # start_urls
        if self.start_urls:
            urls = urls.union(self.start_urls)
        
        # go
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
        ''' make a request from url  using rules in callback_from url '''
        callback = self.callback_from_url(url)
        if callback:
            return scrapy.Request(url, callback=callback)
        return None

    def callback_from_url(self, url):
        """
        determine parse method from url
        """
        return None


    def go(self, category, levelname, default=False):
        ''' check switch of level on category if no explict set in kwargs, return default'''
        if default:
            nocat = "no"+category
            return not (nocat  in self.kwargs and levelname in self.kwargs[nocat])
        else:
            return category in self.kwargs and levelname in self.kwargs[category]


    def get(self, name):
        '''  get value of param, result is list'''
        if name in self.kwargs:
            return self.kwargs[name].split(',')
        else:
            return []
