

from . import *
from ..util import reparts

class Gallery(Item):
    url = Field()
    name = Field()
    description = Field()

    author_url = Field()
    author_name = Field()

    parent_url = Field()  # parent gallery/folder
    parent_id = Field()

    

class Art(Item):
    url = Field()

    name = Field()
    description = Field()

    author_name = Field()
    author_url = Field()

    tag_names = Field()
    category_names = Field()

    thumb_url = Field({'file_url': {'path': 'thumb_path', 'cb': 'thumb_path_cb' }})
    thumb_path = Field()

    image_url = Field({'file_url': {'path': 'image_path'}})
    image_path = Field()

    file_url = Field({'file_url': {'path': 'file_path', 'cb': 'file_path_cb'}})
    file_path = Field()

    gallery_url = Field()
    

    def thumb_path_cb(self, url):
        '''http://t02.deviantart.net/QJzvas6nuAgq9314wGysCMRbp0A=/300x200/filters:fixed_height(100,100):origin()/pre01/9870/th/pre/f/2015/317/5/1/yuna___summoner_costume_by_moogleoutfitters-d9gjd2t.png ->  t02.deviantart.net/pre/f/2015/317/5/1/yuna___summoner_costume_by_moogleoutfitters-d9gjd2t.png '''
        return reparts(url,  [2,9,10,11,12,13,14,15], '/')
        
    def file_path_cb(self, url):
        '''http://www.deviantart.com/download/437347966/dance_party_ia___download_by_sapphirerose_chan-d78dvum.zip?token=f8193e72f5360fb06863b0d32944791cf8f60ddb&ts=1464720719  -> www.deviantart.com/download/437347966/dance_party_ia___download_by_sapphirerose_chan-d78dvum.zip'''
        url = url.split('?')[0]
        return '/'.join(url.split('/')[2:])