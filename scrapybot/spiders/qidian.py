from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapybot.items.qidian import *
import re

#class QidianSpider(CrawlSpider):
class QidianSpider(BaseSpider):
    name = 'qidian'
    allowed_domains = ['qidian.com']
    start_urls = ['http://all.qidian.com/book/bookstore.aspx']
	#    start_urls.extend([ 'http://all.qidian.com/book/bookstore.aspx?PageIndex=%s'%n for n in range(2,1001)])
    print start_urls
    rules = (
    #        Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse(self, response):
		return self.parse_start_url(response)

    def parse_start_url(self, response):
        return self.parse_article_list(response)

    def parse_article_detail(self, response):
        hxs = HtmlXPathSelector(response)
        i = response.meta['article']
        i['description'] = self.extract(hxs, '//span[@itemprop="description"]/text()')
        print i['description']
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
            yield Request('http://all.qidian.com'+i['url'], meta={'article':i},callback=self.parse_article_detail)


    def parse_user(self, response):
        pass

    def extract(self, hxs, xpath, defv=None):
        arr = hxs.select(xpath).extract()
        return arr and arr[0] or defv
