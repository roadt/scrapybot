import logging
logger = logging.getLogger(__name__)
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware

class RedirectDownloaderMiddleware(RedirectMiddleware):

    def __init__(self, settings):
        super(RedirectDownloaderMiddleware, self).__init__(settings)

    def process_request(self, request, spider):
        logger.info("%s:%s %s" % (type(self).__name__,  'process_request',  [request, spider])) 
        return None

    def process_response(self, request, response, spider):
        logger.info("%s:%s %s" % (type(self).__name__,  'process_response',  [request, response, spider, response.headers])) 
        logger.info("%s:%s %s" % (type(self).__name__,  'process_response test',  ['Location' in response.headers,  response.headers.get('Location')]))
        return self._super().process_response(request, response, spider);

    def process_exception(self, request, exception, spider):
        logger.info("%s:%s %s" % (type(self).__name__,  'process_exception',  [request, exception, spider])) 
        return None

    def _super(self):
        return super(RedirectDownloaderMiddleware, self)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
