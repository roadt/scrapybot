# Scrapy settings for scrapybot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#


import sys, os

def getenv(name, default=None):
    return os.environ.get(name) or default



BOT_NAME = 'scrapybot'

SPIDER_MODULES = ['scrapybot.spiders']
NEWSPIDER_MODULE = 'scrapybot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapybot (+http://www.yourdomain.com)'
USER_AGENT  = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2"


COOKIES_ENABLED = True
#COOKIES_DEBUG = True


############  Pipelines Section ##############
ITEM_PIPELINES = {
#    'scrapybot.pipelines.ScrapybotPipeline',
    'scrapybot.pipelines.file.YAFilePipeline' : 10,
    'scrapymongo.pipelines.MongoPipeline' : 20,
}


# for scrapymongo.pipelines.MongoPipeline
MONGO_PIPELINE_HOST =  getenv('MONGO_PIPELINE_HOST', 'localhost')
MONGO_PIPELINE_DBNAME = getenv('MONGO_PIPELINE_DBNAME', 'scrapy')
FILES_STORE = getenv('FILES_STORE', os.path.join(getenv('HOME'), MONGO_PIPELINE_DBNAME))
FILES_URLS_FIELD= getenv('FILES_URLS_FIELD', 'image_urls')
FILES_RESULT_FIELD= getenv('FILES_RESULT_FIELD', 'images')
FILES_EXPIRES= getenv('FILES_EXPIRES', 90)


#FILES_EXPIRES = 90
#IMAGES_EXPIRES = 30


##### downloader

DOWNLOAD_DELAY = 1.5
DOWNLOAD_WARNSIZE=100*1024*1024

DOWNLOADER_MIDDLEWARES = {
#    'scrapybot.downloadermiddlewares.hello.HelloDownloaderMiddleware': 800,
#    'scrapybot.downloadermiddlewares.redirect.RedirectDownloaderMiddleware': 600,
}

DOWNLOADER_MIDDLEWARES_BASE = {
    # Engine side
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
    # Downloader side
}

##### dupfitler
#DUPEFILTER_CLASS = 'scrapymongo.cache.CacheDupeFilter'
DUPEFILTER_DEBUG=True
JOB_DIR= os.path.join(FILES_STORE, 'jobs')
##### downloader middleware
#HTTPCACHE_ENABLED = True
HTTPCACHE_IGNORE_HTTP_CODES=[302]
HTTPCACHE_STORAGE = 'scrapymongo.cache.MongoCacheStorage'


# RedirectMiddleware
REDIRECT_ENABLED = True


# MediaPipeline
MEDIA_ALLOW_REDIRECTS = True
