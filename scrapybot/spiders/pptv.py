# -*- coding: utf-8 -*-
import scrapy
import logging
import urllib.parse
from scrapybot.items.pptv import *
from scrapybot.spiders import *
from scrapybot.util import *

from scrapy.utils.misc import load_object

logger = logging.getLogger(__name__)



class PPTVSpider(ArgsSupport, scrapy.Spider):
    '''
    pptv spider
    '''

    name = "pptv"
    allowed_domains = ["pptv.com"]

    def __init__(self, *args, **kwargs):
        super(PPTVSpider, self).__init__(*args, **kwargs)


    def callback_from_url(self, url):
        """
        determine parse method from url
        """
        if url.startswith('http://list.pptv.com/?'):
            return self.parse_video_list
        if url.startswith('http://list.pptv.com/channel_list.html'):
            return self.parse_video_list_xhr
        if url.startswith('http://v.pptv.com/page/'):
            return self.parse_video
        return None


    def go_next(self, levelname):
        return 'next' in self.kwargs and levelname in self.kwargs['next']

    def go_rlevel(self, levelname):
        return 'rlevel' in self.kwargs and levelname in self.kwargs['rlevel']


    def parse_video_list(self, response):
        part = urllib.parse.urlsplit(response.url)
        yield scrapy.Request('http://list.pptv.com/channel_list.html?' + part.query, callback=self.parse_video_list_xhr)

    def parse_video_list_xhr(self, response):
        # parse video list
        for sel in response.css('li'):
            v = Anim()
            logger.debug("%s:%s %s" % (type(self).__name__,  'parse_video_list_xhr',  [self.kwargs, sel]))

            v['url'] = sel.css('.ui-btn a.detailbtn::attr("href")').extract_first()
            
            v['thumb_url'] = sel.css('.ui-pic img::attr("data-src2")').extract_first()
            v['play_url'] = sel.css('a.ui-list-ct::attr("href")').extract_first()
            v['name'] = sel.css('.ui-txt .main-tt::text').extract_first()
            v['rate_avg'] = tofloat(sel.css('.ui-txt em::text').extract_first())
            v['video_count'] = toint(le(sel.css('.ui-pic .msk-txt').re('[0-9]+'), 0))
            v['completed'] = bool(sel.css('.ui-pic .msk-txt').re('完'))
            yield v

            # whether go to video info page to dig more?
            if self.go_rlevel('video'):
                r =  scrapy.Request(v['url'], callback=self.parse_video)
                r.meta['video'] = v
                yield r

        # next page check & url-generation
        if self.go_next('vlist') and not len(response.css('li')) < 42:
            res = urllib.parse.urlsplit(response.url)
            param_dict = urllib.parse.parse_qs(res.query)
            v = param_dict.get('page')
            if v:
                v[0] = incr(v[0])
            else:
                param_dict['page'] = [2]
            new_query = unparse_qs(param_dict)
            next_page_url = urllib.parse.urlunsplit((res.scheme, res.netloc, res.path, new_query, ''))
            logger.debug("%s:%s %s" % (type(self).__name__,  'parse_video_list_xhr',  [self.kwargs, next_page_url]))
            yield scrapy.Request(next_page_url, callback=self.parse_video_list_xhr)

        

    def parse_video(self, response):
        v = response.meta.get('video') or Anim()
        v['url'] = response.url.split('?')[0]

        v['cover_url'] = response.css('.cover-a img::attr("data-src2")').extract_first() or response.css('.module-dpage-banner a img::attr("src")').extract_first()

        v['name'] = response.css('.module-dpage-info .hd h3::text').extract_first()

        for li in response.css('.infolist > ul li'):
            name = li.xpath('text()').extract_first()
            logger.debug("%s:%s %s" % (type(self).__name__,  'parse_video',  [self.kwargs, v, li]))

            if name == '评分：':
                pass
            elif name == '声优：':
                pass
            elif name == '监督：':
                v['director_names'] = li.css('a::text').extract()
            elif name == '地区：':
                v['area_name'] = li.css('a::text').extract_first()
            elif name == '类型：':
                v['tag_names'] = li.css('a::text').extract()
            elif name == '上映：':
                v['date_publish'] = li.css('a::text').extract_first()
            elif '片长' in name:
                v['duration'] =  int(li.re('[0-9]+')[0])
            elif '播放' in name:
                v['play_count'] = float(li.re('[0-9.]+')[0])*10000
                
        v['video_count'] = response.css('.status p a::text').extract_first() or le(response.css('.dpage-nav .now::text').re('[0-9]+'), 0) or 1
        v['completed'] = bool(response.css('.status p::text').re('完'))
        v['rate_avg'] = tofloat(response.css('.infolist .score::text').extract_first())
        v['actor_names'] = response.css('.infolist .actor a::text').extract()
        v['play_urls'] = response.css('.j_videoSite a::attr("href")').extract() or response.css('#juji_1 a::attr("href")').extract()
       #v['tag_names'] = response.css('.module-bread-nav a::text').extract()
 
        v['description'] = response.css('#video_intro div dd::text').extract_first()
        yield v
        

        