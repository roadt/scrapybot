# Scrapy settings for scrapybot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'scrapybot'

SPIDER_MODULES = ['scrapybot.spiders']
NEWSPIDER_MODULE = 'scrapybot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapybot (+http://www.yourdomain.com)'
USER_AGENT  = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2"


COOKIES_ENABLED = True
#COOKIES_DEBUG = True


############  Pipelines ##############
ITEM_PIPELINES = [
#    'scrapybot.pipelines.ScrapybotPipeline',
	'scrapymongo.pipelines.MongoPipeline'
]

# for scrapymongo.pipelines.MongoPipeline
MONGO_PIPELINE_DBNAME = 'scrapy'




########## downloader #############

DOWNLOAD_DELAY = 0
