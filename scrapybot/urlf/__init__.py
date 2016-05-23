

import re
from functools import partial


def scheme(url, **kwargs):
    schemes =   'scheme' in kwargs and kwargs['scheme'].split(',') or ['http','https']
    return any(map(lambda scheme: url.startswith(scheme+'://'), schemes))


def regex(url, **kwargs):
    exprs =   'regex' in kwargs and kwargs['regex'].split(',') or []
    def check(url, expr):
        return bool(re.search(expr, url))
    return any(map(partial(check, url), exprs))