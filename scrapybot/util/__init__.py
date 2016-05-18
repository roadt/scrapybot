


def incr(s):
    i = int(s)
    i = i + 1
    return str(i)


def unparse_qsl(l):
    l = map(lambda t:  "%s=%s" % t, l)
    return '&'.join(l)

def unparse_qs(d):
    params = []
    for k in d:
        v = d[k]
        for p in v:
            params.append("%s=%s" %(k,p))
    return '&'.join(params)

        
    
def le(l, idx):
    if l is None or idx >= len(l):
        return None
    return l[idx]

def to(o, type):
    if o is None:
        return None
    return type(o)

def toint(o):
    return to(o, int)

def tofloat(o):
    return to(o, float)