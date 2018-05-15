# -*- coding: utf-8 -*-
import sys,os
import re
import scrapy
import logging
import urllib.parse
from scrapybot.items.deviantart import *
from scrapybot.spiders import *
from scrapybot.util import *

from scrapy.utils.misc import load_object

logger = logging.getLogger(__name__)



class DeviantArtSpider(ArgsSupport, scrapy.Spider):
    '''
     spider for deviantart.com
    '''
    name = "devart"
    allowed_domains = ["deviantart.com"]

    def __init__(self, *args, **kwargs):
        super(DeviantArtSpider, self).__init__(*args, **kwargs)

    def callback_from_url(self, url):
        """
        determine parse method from url
        """
        if re.search("https?://(.*).deviantart.com/gallery/.*", url):
            return self.parse_gallery_page
        if re.search("https?://(.*).deviantart.com/favourites/(.*)$", url):
            return self.parse_favorites_page
        if re.search("https?://(.*).deviantart.com/art/(.*)", url):
            return self.parse_art_page


    def parse_gallery_page(self, response):
        # basic info
        g = Gallery()
        g['url'] = response.url
        g['name'] = response.css('.folderview .folderview-top .folder-title::text').extract_first() or response.css('head title::text').extract_first()
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

    def parse_folderview(self, response):
        g = response.meta.get('g')
        # arts
        for sel in response.css('.folderview-art .torpedo-container .thumb'):
            # skip dead art
            if sel.css('.tt-dead'):
                continue
            # valid
            a = Art()
            a['url']  = sel.css('a::attr("href")').extract_first()

            a['name'] = sel.css('.info .title').xpath('.//text()').extract_first()
            a['thumb_url'] = sel.css('.torpedo-thumb-link img::attr("src")').extract_first()
            a['author_name'] = sel.css('.info .extra-info .artist::text').extract_first()  or (g and g.get("author_name"))
            a['author_url'] = sel.css('.info .extra-info .artist a::attr("href")').extract_first()  or (g and g.get("author_url"))
            
            a['gallery_url'] = g and g.get('url')
            if self.go('model', 'art', True):
                yield a

            # scrap art detail  page
            if self.go('rlevel', 'art', False):
                r = scrapy.Request(response.urljoin(a['url']), callback=self.parse_art_page)
                r.meta['art'] = a
                yield r
        
        # next
        if self.go('next', 'alist', True):
            url = response.css('.pagination .next a::attr("href")').extract_first()
            yield scrapy.Request(response.urljoin(url), callback=self.parse_folderview, meta={'g':g})


        
    def parse_favorites_page(self, response):
        # folderview (i.e. arts)
        for e in self.parse_folderview(response):
            yield e
        
        #children favs
        if self.go('rlevel', 'fchild', True):
            for url in response.css('.gr-box .gr-body a::attr("href")').extract():
                abs_url = response.urljoin(url)
                if self.callback_from_url(abs_url) == self.parse_gallery_page:
                    r = scrapy.Request(response.urljoin(url), callback=self.parse_favorites_page)
                    yield r

    def parse_art_page(self, response):
        # art info
        if not response.css('.dev-view-deviation .devpage_gate'): 
            a = response.meta.get('art') or Art()
            a['url']  = response.request.url
            
            a['name'] = response.css('.dev-title-container h1 a::text').extract_first()
            a['author_name'] = response.css('.dev-title-container h1 .username::text').extract_first()
            a['author_url'] = response.css('.dev-title-container h1 .username::attr("href")').extract_first()

            a['image_url'] = response.css('.dev-view-deviation img::attr("src")').extract_first()

            a['description'] = response.css('.dev-description .text').extract_first()
            a['cat_names'] = response.css('.dev-about-cat-cc a span::text').extract()

            def lstrip_tags(tags):
                if tags:
                    return list([t.lstrip('#') for t in tags])

            a['tag_names'] = lstrip_tags(response.css('.dev-about-tags-cc .discoverytag::text').extract())
            a['file_url'] = response.css('.dev-page-download::attr("href")').extract_first()

            if self.go('model', 'art', True):
                yield a
        
        # more from artist
        if self.go('sect', 'more_from_artist', False) and self.go('rlevel', 'art', False):
            for url in response.css('.more-from-artist-title').xpath('following-sibling::div[position()=1]').css('.stream a::attr("href")').extract():
                r = scrapy.Request(response.urljoin(url), callback=self.parse_art_page)
                yield r
                
        # feature_in_fav
        if self.go("sect", "feature_in_fav", False):
            
            if self.go('rlevel', 'art', False):
                for url in response.css('.more-from-collection-preview-row .thumb a::attr("href")').extract():
                    r = scrapy.Request(response.urljoin(url), callback=self.parse_art_page)
                    yield r                
                
            if self.go('rlevel', 'favorite', False):
                for url in response.css('.more-from-collection-preview-row a.collection-name::attr("href")').extract():
                    r = scrapy.Request(response.urljoin(url), callback=self.parse_favorites_page)
                    yield r

                
        # more from devianart
        if self.go('sect', 'more_from_da', False) and self.go('rlevel', 'art', False):
            for url in response.css('.more-from-da-title').xpath('following-sibling::div[position()=1]').css('.stream a::attr("href")').extract():
                r = scrapy.Request(response.urljoin(url), callback=self.parse_art_page)
                yield r
            



            
        