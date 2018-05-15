

import sys, os
import unittest
import scrapy
from test import (fixture, config, assertion)

# add project dir into serach path
#dirname=os.path.dirname
#sys.path.append(dirname(dirname(__file__)))

# import spider , item def
from scrapybot.spiders.deviantart import *
from scrapybot.items.deviantart import *

class  DevaintArtSpiderTestCase(unittest.TestCase, assertion.ItemAssertion):

    def setUp(self):
        self.fixtures = fixture.FixtureManager(config.deviantart_fixtures)
        self.fixtures.download_fixtures()
        self.spider = DeviantArtSpider()


    def test_parse_gallery_page(self):
        '''
        spider.parse_gallery_page
        '''
        resp = self.fixtures.get_fixture_response('gallery_normal')
        result = list(self.spider.parse_gallery_page(resp))
        print(result)
        
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)


        #
        gallery_required_fields = ['url', 'name', 'author_url', 'author_name']
        art_required_fields = ['url', 'name', 'author_name', 'author_url']
        art_special_fields = ['thumb_url', 'gallery_url']

        for obj in result:
            if isinstance(obj, Art):
                self.assertItemRequired(obj, art_required_fields + art_special_fields)
            if isinstance(obj, Gallery):
                self.assertItemRequired(obj, gallery_required_fields)

    def test_parse_art_page(self):
        '''
        spider.parse_art_page
        '''
        resp = self.fixtures.get_fixture_response('art_normal')
        objs = list(self.spider.parse_art_page(resp))

        self.assertIsNotNone(objs)
        self.assertGreater(len(objs), 0)

        art_required_fields = ['url', 'name', 'author_name', 'author_url']
        art_special_fields = [ 
            'description', 
            'image_url',
            'cat_names',
            # 'tag_names',   - some page doesn't have tag name
            'file_url',
        ]
        for obj in objs:
            if isinstance(obj, Art):
                self.assertItemRequired(obj, art_required_fields + art_special_fields)

        

    @unittest.skip('test_parse_match_page')
    def test_parse_match_page(self):
        resp  = self.fixtures.get_fixture_response('soccer_match')
        items = list(self.spider.parse_match_page(resp))

        self.assertGreater(len(items), 0)
        for item in items:
            self.assertItem(item)


