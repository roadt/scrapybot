# -*- coding: utf-8 -*-
import sys,os
import re
import scrapy
import logging
import urlparse
from scrapybot.items.wdj import *
from scrapybot.spiders import *
from scrapybot.util import *

from scrapy.utils.misc import load_object

logger = logging.getLogger(__name__)

class WandoujiaSpider(ArgsSupport, scrapy.Spider):
    '''
     spider for wandoujia.com
    '''
    name = "wdj"
    allowed_domains = ["wandoujia.com"]

    def __init__(self, *args, **kwargs):
        super(WandoujiaSpider, self).__init__(*args, **kwargs)


    def callback_from_url(self, url):
        """
        determine parse method from url
        """
        return None


