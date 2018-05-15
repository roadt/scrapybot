


import os
import unittest
from test import fixture



class FixtureTestCase(unittest.TestCase):


    def setUp(self):
        self.settings = [
            {
                'name':'test01',
                'url': 'http://example.org'
            },
            {
                'name': 'test02',
                'url': 'http://example.com/'
            }
        ]

        self.fixturemgr = fixture.FixtureManager(self.settings)
        self.test_get_download_fixtures()


    def test_get_download_fixtures(self):
        self.fixturemgr.download_fixtures()
        for fixture in self.fixturemgr.fixtures:
            self.assertTrue(os.path.exists(fixture['path']))

    def test_get_fixture_response(self):
        setting = self.settings[0]
        resp = self.fixturemgr.get_fixture_response(setting['name'])
        self.assertIsNotNone(resp)
        self.assertEqual(resp.url, setting['url'])


    def test_remove_download(self):
        self.fixturemgr.remove_download()
        for fixture in self.fixturemgr.fixtures:
            self.assertFalse(os.path.exists(fixture['path']))


