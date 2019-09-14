# -*- coding: utf-8 -*-
import sys,os
import re
import scrapy
import logging
import urllib.parse
from scrapybot.items.zdic import *
from scrapybot.spiders import *
from scrapybot.util import *

from scrapy.utils.misc import load_object

logger = logging.getLogger(__name__)


class ZDicSpider(ArgsSupport, scrapy.Spider):
    ''' zdic spider '''
    name = "zdic"
    allowed_domains = ["zdic.net"]
    start_urls = ['https://www.zdic.net/zd/bs/']

    hzs_cc1_url = 'http://www.zdic.net/zd/zb/cc1'
    hzs_cc2_url = 'http://www.zdic.net/zd/zb/cc2'
    hzs_ty_url = 'http://www.zdic.net/zd/zb/ty'

    def __init__(self, *args, **kwargs):
        super(ZDicSpider, self).__init__(*args, **kwargs)

    def callback_from_url(self, url):
        """
        determine parse method from url
        """

        #http://www.zdic.net/zd/zb/cc1
        if re.search("https?://www.zdic.net/zd/zb", url):
            return self.parse_z_zb_page

        #http://www.zdic.net/hans/一
        if re.search("https?://www.zdic.net/hans/", url):
            return self.parse_hans_page

        return None

    def parse_hans_page(self, response):
        hz = Hanzi()
        hz['url'] = response.url

        # 基本信息
        #einfo = response.css('#ziif #z_i_1')
        hz['thumb_url'] =  response.urljoin(response.css('#bhbs::attr("src")').extract_first())
        hz._headers  = { 'Referer' : response.url }  #thumb_url need referere

        # piyin
        for e in response.css('.z_py .song'):
            hz['py_name'] = e.xpath('text()').extract_first()
            hz['py_url'] = response.urljoin(e.css('a::attr("data-src-mp3")').extract_first())
            hz['py_audio_url'] = hz['py_url']
            #hz['py_audio_url'] = 'http://www.zdic.net/p/mp3/%s.mp3' % re.search('spz\("(.*)"\)', e.css('script::text').extract_first()).group(1) 
            
            # break, only 1st for now.
            break

        # zhuyin
        for e in response.css('.z_zy .song'):
            hz['py_name'] = e.xpath('text()').extract_first()

            break

        # bushou
        bs = response.css('.z_bs2 p')
        hz['bs'] = bs[0].css('a::text').extract_first()
        hz['bw'] = toint(bs[1].xpath('text()').extract_first())
        hz['zbh'] = toint(bs[2].xpath('text()').extract_first())
        hz['zxfx'] = response.css('.dsk .dsk_2_1::text').extract_first()
        hz['bsn'] = response.css('.dsk .z_bis2 p::text').extract_first()

        #yitizhi
        hz['ytz'] = response.css('.z_ytz2 a::text').extract() + response.css('.z_ytz2 a .ytz_txt::text').extract()

        # IM
        ims = response.css('.dsk .dsk_2_1 p::text').extract()
        hz['im_unicode'] =  ims[0]
        hz['im_wubi'] = ims[1]
        hz['im_changjie'] = ims[2]
        hz['im_zhengma'] = ims[3]
        hz['im_sijiao'] = ims[4]
        
        yield hz
        

    def parse_z_zb_page(self, response):
        for e in response.css('.bs_index3 a'):
            hz = Hanzi()
            hz['url'] = scrapy.Request(response.urljoin(e.xpath('@href').extract_first())).url
            hz['name'] = e.xpath('text()').extract_first()
            if self.go('model', 'hanzi', True):
                yield hz
            
            if self.go('rlevel', 'hanzi', False):
                yield scrapy.Request(hz['url'], callback=self.parse_hans_page)
        

    def parse_subcate_page(self, response):
        # basic info
        g = Gallery()
        g['url'] = response.url
        g['name'] = response.css('.folderview .folderview-top .folder-title::text').extract_first()
        g['description'] = response.css('.folderview .folderview-top .description::text').extract_first()
        g['author_url'] = response.css('.catbar a.username::attr("href")').extract_first()
        g['author_name'] = response.css('.catbar .username::text').extract_first()
        g['parent_url'] = response.css('.folderview .folderview-top h1').xpath('a[last()]/@href').extract_first()
        
        if self.go('model', 'gallery', True):
            yield g
        
        # folderview (i.e. arts)
        response.meta['g'] = g
        for e in self.parse_folderview(response):
            yield e
        

        #children galleries
        if self.go('rlevel', 'gchild', True):
            for url in response.css('.gr-box .gr-body .gr  a::attr("href")').extract():
                abs_url = response.urljoin(url)
                if self.callback_from_url(abs_url) == self.parse_gallery_page:
                    r = scrapy.Request(abs_url, callback=self.parse_gallery_page)
                    yield r


