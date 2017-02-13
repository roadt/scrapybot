

from . import *
from ..util import reparts

class Product(Item):
    name = Field()
    url = Field()

    price_ref = Field()

