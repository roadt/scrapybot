# -*- coding: utf-8 -*-
import sys,os
import re
import scrapy
import urllib.parse
from scrapybot.items import *
from scrapybot.spiders import *
from scrapybot.util import *
from scrapy.utils.misc import load_object

import logging
logger = logging.getLogger(__name__)



class StashSpider(ArgsSupport, scrapy.Spider):
    '''
     spider for deviantart.com
    '''
    name = "stash"
    allowed_domains = ["sta.sh"]
    #handle_httpstatus_list =  (301, 302, 303, 307, 308)


    def __init__(self, *args, **kwargs):
        super(StashSpider, self).__init__(*args, **kwargs)

    def callback_from_url(self, url):
        """
        determine parse method from url
        """
        if re.search("https?://sta.sh/[^/]+$", url):
            return self.parse_file_page

    def parse_file_page(self, response):
        
        item = File()
        item['url']  = response.url
        item['name'] = response.css('.dev-view-main-content .dev-title-container >  h1 > a::text').extract_first()
        item['author_name'] = response.css('.dev-view-main-content .dev-title-container >  h1 .username::text').extract_first()
        item['author_url'] = response.css('.dev-view-main-content .dev-title-container >  h1 .username::attr("href")').extract_first()

        item['file_url'] = response.css('.dev-view-meta-content  .dev-page-button::attr("href")').extract_first()
        #item._headers  = { 'Referer': response.url, 'Cookie' : response.headers[b'Set-Cookie'] }  #thumb_url need referere
        item['file_ext'] = response.css('.dev-page-download .text::text').extract_first().split(' ')[0].lower()
        
        for  dt in  response.css('.dev-view-meta-content  .dev-metainfo-details dt'):
            name = dt.xpath('text()').extract_first().strip()
            if name == 'Uploaded on':
                item['date_uploaded'] = dt.xpath('following-sibling::dd/span/@ts').extract_first()
            if name == 'File Size':
                item['file_size'] = dt.xpath('following-sibling::dd/text()').extract_first()

        yield item

        #manual send download request
        #yield scrapy.Request(item['file_url'], callback=self.parse_file_download, meta = { 'item': item })

    def parse_file_download(self, response):
        item = response.meta['item']
        logger.debug("%s:%s %s" % (type(self).__name__,  'parse_file_download', [response, response.headers]))
        filename = self.filename_from_response(response)

        logger.debug("%s:%s %s" % (type(self).__name__,  'file name', [response.headers.get("Content-Disposition"), filename]))
        file_path = os.path.join(item.file_path_cb(item['file_url']) , filename)
        item['file_path'] = file_path
        self.write2file(response.body, os.path.join(self.settings.get('FILES_STORE'), file_path))
        yield item
        
    def write2file(self, data, filepath):
        os.makedirs(os.path.dirname(filepath))
        with open(filepath, 'wb+') as f:
            f.write(data)
        
    def filename_from_response(self, response):
        content_disposition = response.headers.get("Content-Disposition");
        filename = re.findall(r'attachment; filename\*?=(.*)', str(content_disposition))[0].split("'")[2]
        return filename
