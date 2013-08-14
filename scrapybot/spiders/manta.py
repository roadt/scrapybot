from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapybot.items.manta import Company

class MantaSpider(CrawlSpider):
    name = 'manta'
    allowed_domains = ['manta.com']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(allow=r"/c/[^/]*/[^/]*$"), callback='parse_company_detail', follow=True)
    )

    def __init__(self, term=None, *args, **kwargs):
        super(MantaSpider, self).__init__(*args, **kwargs)
        if term:
            self.start_urls = ['http://www.manta.com/mb?search=%s' % term]
        else:
            self.start_urls = ['http://www.manta.com/']

    def parse_start_url(self, response):
        return self.parse_company(response)

    def parse_search_result(self, response):
        hxs = HtmlXPathSelector(response)
        elems = hxs.select('//a[contains(@class, "nextYes")]/@href').extract()
        if len(elems)>=1:
            yield Requeset(elems[0], callback=self.parse_company)

    def parse_company(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        for h in hxs.select('//div[contains(@class, "pbl")]'):
            c =  Company()
            c['name'] = h.select('*/h2[@itemprop="name"]/a/text()').extract()
            c['manta_url'] = h.select('*/h2[@itemprop="name"]/a/@href').extract()
            c['street'] = h.select('*/div[@itemprop="streetAddress"]/text()').extract()
            c['locality'] =h.select('*/div[@itemprop="addressLocality"]/text()').extract()
            c['region'] =h.select('*/div[@itemprop="addressRegion"]/text()').extract()
            c['postal_code'] =h.select('*/div[@itemprop="postalCode"]/text()').extract()
            c['phone'] =h.select('*/div[@itemprop="telephone"]/text()').extract()
            c['website'] = h.select('*/div[@itemprop="url"]/text()').extract()
            yield c

    def parse_company_detail(self, response):
        print response
