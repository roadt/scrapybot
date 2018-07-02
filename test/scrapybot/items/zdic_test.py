

import sys, os
import unittest
import scrapy
#from test import (fixture, config, assertion)

from scrapybot.items.zdic import *

class ZDicItemTestCase (unittest.TestCase):

    def test_field(self):
        hz1 = Hanzi()
        print(hz1['image_url'])
        self.assertIsNotNone(hz1['image_url'])





        

