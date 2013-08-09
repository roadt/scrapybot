from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapybot.items import *

class QidianSpider(CrawlSpider):
    name = 'qidian'
    allowed_domains = ['qidian.com']
    start_urls = ['http://all.qidian.com/Default.aspx']

    rules = (
    #        Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_article_list(response)

    def parse_article_list(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        for h in hxs.select('//div[contains(@class,"sw1") or contains(@class,"sw2")]'):
            i = Article()
            i['title'] = h.select('div[@class="swb"]/span/a/text()').extract();
            i['url'] = h.select('div[@class="swb"]/span/a/@href').extract();
            i['author_name'] = h.select('div[@class="swd"]/a/text()').extract();
            i['author_url'] = h.select('div[@class="swd"]/a/@href').extract();
            i['char_count'] = h.select('div[@class="swc"]/text()').extract();
            i['last_update'] = h.select('div[@class="swe"]/text()').extract();
            yield Request(i['author_url'][0],callback=self.parse_user)
            yield i

    def parse_user(self, response):
        pass
