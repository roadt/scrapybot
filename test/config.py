

#
#  all configuration about tests
#



# deviantart fixtures
deviantart_fixtures = [
    {        'name': 'gallery_normal',        'url':'http://diemdo-shiruhane.deviantart.com/gallery/'   },
    {        'name': 'art_normal',        'url':'http://diemdo-shiruhane.deviantart.com/art/Vacation-house-in-Ocean-MMD-Stage-DL-352517288' },
]


# load from yaml file
from os.path import dirname, join
import yaml

def yaml_config():
    with open(join(dirname(__file__), 'config.yml')) as f:
        return yaml.load(f)

