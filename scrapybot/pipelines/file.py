
from scrapy.pipelines.files  import *
from scrapy import *


class YAFilePipeline(FilesPipeline):
    '''
    Yet another File  pipeline. 
    
    configure the file_url in Field with 'file_url'. like following.
    
    class YourItem(Item):
        cover_url = Field({file_url: {path: file_path, cb: 'url_to_path'}})
        file_path = Field()

         def url_to_path(url): # calcualte store location of downloaded file.
               return os.path.join('files', url.split('?')[0].split('/')[-1])

    then the pipleline will download the file that value of cover_url indicates.
    and store local path of the donwloaded file into 'file_path' field.
    the locale path is calculated by 'url_to_path' , if cb is omit, then the local path is url that remove 'schema://'.
    i.e.   http://image.cmfu.com/books/1001396288/1001396288.jpg -> image.cmfu.com/books/1001396288/1001396288.jpg -> 

    '''
    def __init__(self, store_uri, download_func=None, settings=None):
        super(YAFilePipeline, self).__init__(store_uri, download_func, settings)

    @classmethod
    def from_settings(cls, settings):
        s3store = cls.STORE_SCHEMES['s3']
        s3store.AWS_ACCESS_KEY_ID = settings['AWS_ACCESS_KEY_ID']
        s3store.AWS_SECRET_ACCESS_KEY = settings['AWS_SECRET_ACCESS_KEY']

        cls.FILES_URLS_FIELD = settings.get('FILES_URLS_FIELD', cls.DEFAULT_FILES_URLS_FIELD)
        cls.FILES_RESULT_FIELD = settings.get('FILES_RESULT_FIELD', cls.DEFAULT_FILES_RESULT_FIELD)
        cls.EXPIRES = settings.getint('FILES_EXPIRES', 90)
        store_uri = settings['FILES_STORE']
        return cls(store_uri, settings=settings)
    
    def get_media_requests(self, item, info):
        requests = []

        for n in item.keys():
            field = item.fields[n]
            if 'file_url' in field and item[n]:  # is file_url field and value not None
                cfg = field['file_url']

                r = Request(item[n])
                r.meta['item'] = item
                r.meta['f_url'] = n
                r.meta['f_path'] = cfg['path']

                # optional
                r.meta['f_cb'] = cfg.get('cb')
                r.meta['f_checksum'] = field.get('checksum')

                # _request headers
                if hasattr(item, '_headers') and item._headers: 
                    r.headers.update(item._headers)

                logger.debug("%s:%s %s, headers: %s" % (type(self).__name__,  'get_media_requests:add_request',  r, r.headers))

                requests.append(r)
        logger.debug("%s:%s %s" % (type(self).__name__,  'get_media_requests',  requests))
        return requests
            
    def file_path(self, request, response=None, info=None):
        try:
            item = request.meta['item']
            path_field = request.meta['f_path']
            path_cb = request.meta['f_cb']  # callback to calcualte path of file in operating file system
            if path_cb and hasattr(item, path_cb):
                path= getattr(item,path_cb)(request.url)
            else:
                params = request.url.split('/')[2:] 
                path  =  os.path.join(*params)
        except StandardError as e:
            logger.error("%s:%s %s %s" % (type(self).__name__,  'file_path',  type(e), item))
        else: 
            logger.debug("%s:%s %s" % (type(self).__name__,  'file_path',  path))
        return path
            
    def media_downloaded(self, response, request, info):
        logger.error("%s:%s headers: %s" % (type(self).__name__,  'media_downloaded',  response.headers)) 
        result = super(YAFilePipeline, self).media_downloaded(response, request, info)
        item = request.meta['item']
        path_field = request.meta['f_path']
        item[path_field] = result['path']
    
        # remeber file_url in result , for later
        reuslt['field'] = request.meta['f_url']
        logger.debug("%s:%s %s" % (type(self).__name__,  'media_downloaded',  result))

        return result

    def item_completed(self, results, item, info):
        #
        #if isinstance(item, dict) or self.FILES_RESULT_FIELD in item.fields:
        #    item[self.FILES_RESULT_FIELD] = [x for ok, x in results if ok]
        logger.debug("%s:%s %s" % (type(self).__name__,  'item_completed', item))

        return item
