import logging
logger = logging.getLogger(__name__)


class HelloDownloaderMiddleware(object):

    def __init__(self, settings):
        pass

    def process_request(self, request, spider):
        logger.info("%s:%s %s" % (type(self).__name__,  'process_request',  [request, spider])) 
        return None


    def process_response(self, request, response, spider):
        logger.info("%s:%s %s" % (type(self).__name__,  'process_response',  [request, response, spider])) 
        return response

    def process_exception(self, request, exception, spider):
        logger.info("%s:%s %s" % (type(self).__name__,  'process_exception',  [request, exception, spider])) 
        return None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
