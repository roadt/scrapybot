

from . import mongodb

def art(**kwargs):
    '''generate urls of art with s= (search text), u= (","-separated author_names), t= (","-separated tags) '''
    with mongodb()  as db:
        cond = {}
        if 's' in kwargs:
            cond['$text'] = { '$search' : kwargs.get('s') }
        if 'u' in kwargs:
            cond['author_name'] = { '$in' : kwargs.get('u').split(',') }
        if 't' in kwargs:
            cond['tag_names'] = { '$in' : kwargs.get('t').split(',') }
        urls = map(lambda e: e['url'], db.art.find(cond, {'url': 1}))
        return { 'url': urls }
                

def art_to_down(**kwargs):
    '''generate urls of art which not yet downloaded
    with s= (search text), u= (","-separated author_names), t= (","-separated tags) '''

    with mongodb()  as db:
        cond = { "file_url" : {'$eq' :None}}
        if 's' in kwargs:
                cond['$text'] = { '$search' : kwargs.get('s') }
        if 'u' in kwargs:
                cond['author_name'] = { '$in' : kwargs.get('u').split(',') }
        if 't' in kwargs:
                cond['tag_names'] = { '$in' : kwargs.get('t').split(',') }
        urls = map(lambda e: e['url'], db.art.find(cond, {'url': 1}))
        return { 'url' : urls}