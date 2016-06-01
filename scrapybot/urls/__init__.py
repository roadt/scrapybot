import contextlib
from pymongo import *
from scrapy.utils.project import inside_project, get_project_settings


@contextlib.contextmanager
def mongodb():
        dbname = get_project_settings().get('MONGO_PIPELINE_DBNAME', 'scrapyh')
        dbhost = get_project_settings().get('MONGO_PIPELINE_HOST', 'localhost')
        clt  = MongoClient(dbhost)
        db = clt[dbname]
        try:
                yield db
        finally:
                clt.close()


def all(**kwargs):  
        '''
        url generator to find all urls match a certain condition from existing records

        e.g.  find out all urls of art page that belongs to author 'decentgirl'
        scrapy crawl devart -a urlg=scrapybot.urls.eh.all -a t=art -a f=auhtor_name -a v=decentgirl

        '''
        
        ty = kwargs['t']
        field = kwargs.get('f')
        value = kwargs.get('v')  # optional, omit mean None
        
        cond  = {}

        # already has url set? then filter based on on it
        url = kwargs.get('url') and kwargs.get('url').split(',')
        if url:
            cond.update({ 'url': {'$in': url }})

        if field:
            cond.update({ field: { "$eq" : value }})

        # 
        with mongodb() as db:
                cur = db[ty].find(cond, { 'url'  : 1})
                urls = map(lambda x: x['url'], cur)
                return { 'url' : urls }

