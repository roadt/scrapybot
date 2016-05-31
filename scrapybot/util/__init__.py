


def incr(s):
    ''' increase by +1 for s'''
    i = int(s)
    i = i + 1
    return str(i)


def unparse_qsl(l):
    '''  join qs list to a url  -  reverse op for urlparse.parse_qsl'''
    l = map(lambda t:  "%s=%s" % t, l)
    return '&'.join(l)

def unparse_qs(d):
    '''  join qs dict to a url  -  reverse op for urlparse.parse_qs'''

    params = []
    for k in d:
        v = d[k]
        for p in v:
            params.append("%s=%s" %(k,p))
    return '&'.join(params)

        
    
def le(l, idx):
    ''' none safty - l[idx] '''
    if l is None or idx >= len(l):
        return None
    return l[idx]

def to(o, type):
    ''' none safty - type(o) '''
    if o is None:
        return None
    return type(o)

def toint(o):
    return to(o, int)

def tofloat(o):
    return to(o, float)


def reparts(s, arr, sep=' '):
    ''' split str and extract specified  parts , to get a new string'''
    parts = s.split(sep)
    length = len(parts)
    parts = [  parts[idx] for idx in arr if idx < length]
    return sep.join(parts)