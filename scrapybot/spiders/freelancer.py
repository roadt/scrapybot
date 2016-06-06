# -*- coding: utf-8 -*-
import sys,os
import re
import scrapy
import logging
import urlparse
from scrapybot.items.freelancer import *
from scrapybot.spiders import *
from scrapybot.util import *

from scrapy.utils.misc import load_object

logger = logging.getLogger(__name__)



class FreelancerSpider(ArgsSupport, scrapy.Spider):
    '''
     spider for freelancer.com
    '''
    name = "freelancer"
    allowed_domains = ["freelancer.com"]

    def __init__(self, *args, **kwargs):
        super(FreelancerSpider, self).__init__(*args, **kwargs)

    def callback_from_url(self, url):
        """
        determine parse method from url
        """
        if re.search("https?://(.*).freelancer.com/jobs/.*$", url):
            return self.parse_jobs_page

    def parse_jobs_page(self, response):
        # jobs
        for  sel  in response.css('table.ProjectTable tbody tr'):
            tds = sel.css('td')
            
            # skip the empty oen
            if not tds[0].xpath('text()'):
                continue
            
            j = Job()
            j['name']  = tds[0].xpath('text()').extract_first().strip()
            j['description'] = tds[1].xpath('text()').extract_first()
            j['bid_count'] = tds[2].xpath('text()').extract_first()
            j['cat_names'] = tds[3].css('a::text').extract()
            #budget
            j['date_started'] = tds[4].xpath('text()').extract_first()
            j['date_end'] = tds[5].xpath('text()').extract_first()
            j['bid_avg'] = tds[6].xpath('text()').extract_first()

            j['url'] = response.urljoin('/projects/%s/%s' % (j['cat_names'][0], j['name'].replace(' ', '-')))
            
            if self.go('model', 'job', True):
                yield j
        
                
        # next
        if self.go('next', 'jlist', True):
            url = response.css('.paginate_button.next a::attr("href")').extract_first()
            yield scrapy.Request(response.urljoin(url), callback=self.parse_jobs_page)


