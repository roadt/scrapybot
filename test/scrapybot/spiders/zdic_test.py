

import sys, os
import unittest
from   unittest import skip
import scrapy
from test import (fixture, config, assertion)

# add project dir into serach path
#dirname=os.path.dirname
#sys.path.append(dirname(dirname(__file__)))

# import spider , item def
from scrapybot.spiders.zdic import *
from scrapybot.items.zdic import *

class  ZdicSpiderTestCase(unittest.TestCase, assertion.ItemAssertion):

    def setUp(self):
        self.fixtures = fixture.FixtureManager(config.yaml_config()['zdic'])
        self.fixtures.download_fixtures()
        self.spider = ZDicSpider()

    def test_parse_z_zb_page(self):
        resp = self.fixtures.get_fixture_response('zdic_z_zb_cc1')
        result = list(self.spider.parse_z_zb_page(resp))
        #print(result)    
        self.assertIn('字', resp.body.decode())
        self.assertGreater(len(result), 0)
        for obj in result:
            assert isinstance(obj, (scrapy.Request, Hanzi))

    def test_pase_z_js_page(self):
        resp = self.fixtures.get_fixture_response('zdic_z_js_738b')
        result = list(self.spider.parse_z_js_page(resp))
        #print(result)    
        self.assertIn('王', resp.body.decode())
        self.assertGreater(len(result), 0)
        hanzi_required_fields = ['url', 'image_url', 'py_name', 'audio_url']
        for obj in result:
            print(obj)
            assert isinstance(obj, (Hanzi))
            self.assertItemRequired(obj, hanzi_required_fields)

    @skip('test_parse_match_page')
    def test_parse_gallery_page(self):
        '''
        spider.parse_gallery_page
        '''
        resp = self.fixtures.get_fixture_response('zdic_z_jbs_bh')
        result = list(self.spider.parse_z_jbs_bh(resp))
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

    @skip('no-reason')
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



