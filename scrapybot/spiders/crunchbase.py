from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import BaseSpider
from scrapy.http import Request
from scrapybot.items.crunchbase import Company, Office, Person
import re


def v(o, idx):
    if o is None:
        return None
    elif isinstance(o, dict):
        return o.get[idx]
    elif isinstance(o, list) and idx < len(o):
        return o[idx]
    else:
        return None




class CrunchbaseSpider(BaseSpider):
    name = 'crunchbase'
    allowed_domains = ['crunchbase.com']
    start_urls = ['http://www.crunchbase.com/companies?q=software']

    url_base = 'http://www.crunchbase.com'

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        for url in hxs.select('//ul[@class="col1_alpha_nav"]/li/a/@href').extract():
            yield Request(self.url_base + url, callback=self.parse_company_list)


    def parse_company_list(self, response):
        hxs = HtmlXPathSelector(response)
        for n in hxs.select('//table[@class="col2_table_listing"]//li/a'):
            i = Company()
            i['name'] = self.extract(n, 'text()')
            url = self.extract(n, '@href')
            i['key'] = re.search("/([^/]+)$", url).group(1)
            yield Request(self.url_base+ url, meta={'company':i}, callback=self.parse_company_detail)

    def parse_company_detail(self,  response):
        hxs = HtmlXPathSelector(response)
        i = response.meta.get('company') or Company()
        i['logo'] = self.extract(hxs, '//div[@id="company_logo"]/a/img/@src')
        i['long_description'] = self.extract(hxs, '//*[@id="col2_internal"]/p')

        general_information =  hxs.select('//h2[text()[normalize-space(.)="General Information"]]/following-sibling::div[position()=1]/table')
        data = self.extract_table(general_information, {'Website':['a/@href'], 'Category':['a/text()'], 'Twitter':['a/@href']})
        i['category'] = v(data.get('Category'), 0)
        i['short_description'] = v(data.get('Description'),0)
        i['founded_date'] = v(data.get('Founded'),0)

        i['website'] = v(data.get('Website'), 0)
        i['blog'] =  v(data.get('Blog'), 0)
        i['twitter'] = v(data.get('Twitter'),0)
        i['phone'] = v(data.get('Phone'),0)
        i['email'] = v(data.get('Email'), 0)
        yield i
        person_div = hxs.select('//*[@id="current_relationships"]/following-sibling::div')
        urls  = person_div.select('div[@class="col1_people_name "]/a/@href').extract()
        names  = person_div.select('div[@class="col1_people_name "]/a/text()').extract()
        titles  = person_div.select('div[@class="col1_people_title "]/text()').extract()
        print((person_div, urls, names, titles))
        for idx in range(len(names)):
            p = Person()
            p['name'] = v(names,idx)
            p['title'] = v(titles,idx)
            p['company_key'] =  i.get('key')
            url = v(urls,idx)
            p['key'] = url
            if not url is None:
                yield Request(self.url_base + url, meta={'person':p}, callback=self.parse_person_detail)
            else:
                print(p)


    def parse_person_detail(self, response):
        hxs = HtmlXPathSelector(response)
        i = response.meta.get('person') or Person()
        i['long_description'] = "\n".join(hxs.select('//h1[@class="h1_first"]/following-sibling::p/text()').extract())
        i['presence'] = ','.join(hxs.select('//h2[text()[normalize-space(.)="Web Presences"]]/following-sibling::div[position()=1]//text()').extract()).strip()
        yield i


    def extract(self, hxs, xpath, defv=None):
        arr = hxs.select(xpath).extract()
        return arr and arr[0] or defv


    def extract_table(self, hxs, cfg={}):
        rows = {}
        for row in hxs.select('tr'):
            tds = row.select('td')
            name = tds[0].select("text()").extract()[0].strip()
            value = None
            if name in cfg:
                xpaths = cfg[name]
                value = [tds[i+1].select(i<len(xpaths) and xpaths[i] or 'text()').extract()[0] for i in range(0, len(tds)-1)]
                rows[name] = value
            else:
                rows[name]  =  [self.extract(x,'text()') for x in tds[1:]]
                return rows
