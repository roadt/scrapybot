
import sys,os
import re
from shovel import task
from pymongo import MongoClient,ASCENDING
from scrapy.utils.project import get_project_settings
from six import print_
from itertools import imap

@task
def lstrip_tag_names():
    '''lstrip "#" of tag_names. i.e.  #mmd -> mmd '''

    settings = get_project_settings()
    files_store = settings.get('FILES_STORE')
    from scrapymongo import mongodb

    with mongodb(settings) as db:
        cur = db.art.find({'tag_names': { '$in': [re.compile('#')]}}, {'url':1,'tag_names':1})
        objs = list(cur)
        print_("Count:%s" % len(objs))
        pcnt = 0
        for obj in objs:
            tag_names = obj['tag_names']
            new_tag_names = list(imap(lambda tag: tag.lstrip('#'), tag_names))
            #print_({'url': obj['url']}, { '$set' : { 'tag_names' : new_tag_names }})
            res = db.art.update({'url': obj['url']}, { '$set' : { 'tag_names' : new_tag_names }})
            print_('.',end='')
            pcnt += 1
        print_("\nDone: %s" %pcnt)
            
            
        


            
    
@task
def remove_fail_cache():
    ''' some fail need remove httpcache entries to recover. 
    classical case is file download url is  extracted  from url with token,but it is downloaded failed. '''
    settings = get_project_settings()
    files_store = settings.get('FILES_STORE')
    from scrapymongo import mongodb

    def is_fail(o):
        ''' something not right to require remove cache to recover'''

        fail = 'file_url' in o and not o.get('file_path') #  detail page scraped, but somehow file is not download, the url easily expried (url with token)
        if fail:
            return 1
        
        with open(os.path.join(files_store, o['file_path']), 'rb') as f:
            fail = (f.read(6) == b'<html>')   # the file is downloaded, but somehow it's a html page  not right picture or archive.

        if fail:
            return 2

    def clear_cache(o):
        # remove file 
        if o.get('file_path'):
            os.remove(os.path.join(files_store, o['file_path']))
        # remove cache
        db.cache.remove({'url': o['file_url']})
        db.cache.remove({'url': o['url']})
        # update art 
        r = db.art.update({'url': o['url']}, {'$set' :{ 'file_url': None, 'file_path': None}})

    
    author_names = set()
    pcnt= 0
    try:
        with mongodb(settings) as db:
            cur = db.art.find({'file_url': {'$ne':None}})
            for o in cur:
                #print_('trying ' + o['file_path'])
                fail = is_fail(o)
                if fail:
                    if o.get('author_name'):
                        author_names.add(o['author_name'])
                    else:
                        print_('error - author_name - %s' % o)
                    clear_cache(o)
                    pcnt+=1
                    print_("%s,%s,%s,[%s]" % (pcnt, o['author_name'], o['url'], fail))
    finally:
        print_("\n\n-------- affected authors ----------")
        print_(','.join(author_names))
        print_("-"*50)

                    
                    
                    
                


        

                
            
            