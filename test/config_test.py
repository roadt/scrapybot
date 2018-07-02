
import os
import unittest
from test import fixture

from  .config import yaml_config

class ConfigTestCase(unittest.TestCase):

    def test_config(self):
        cfg = yaml_config()
        self.assertTrue('zdic' in cfg)







