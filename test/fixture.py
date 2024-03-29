

__description__ = '''
fixture configuration and utilities.

steps to use:
configure new fixture config in FIXTURES

call download_fixtures to download html and store it.
import .fixture 

'''

import sys, os
import urllib.request, urllib.parse, urllib.error
from  scrapy.http import request, response



class FixtureManager():

    def __init__(self, fixtures):
        # if path is None, fill it
        self.fixtures = fixtures
        for fixture in fixtures: 
            name = fixture['name']
            url = fixture['url']
            path = fixture.get('path')
            if not path:
                # use name to generate a path
                path = os.path.join(os.path.dirname(__file__), 'fixtures', '%s.%s'%(name,'html'))
                fixture['path'] = path
            else:
                # if not abs , convert to abs
                if not os.path.isabs(path):
                    path = os.path.abspath(path)
                    fixture['path'] = path
        
        
    def remove_download(self, fixtures=None):
        '''
        remove files that is download
        '''
        fixtures = fixtures or self.fixtures
        for fixture in fixtures: 
            path = fixture['path']
            if os.path.abspath(path):
                os.remove(path)
        

    def download_fixtures(self, fixtures=None):
        '''
        download html file from url of fixture
        '''
        fixtures = fixtures or self.fixtures
        for fixture in fixtures: 
            name = fixture['name']
            url = fixture['url']
            path = fixture['path']

            # download
            if not os.path.exists(path):
                urllib.request.urlretrieve(url, path)

    def get_fixture_response(self, name):
        '''
        get config using name and make a response for unit test purpose
        '''
        for fxt in self.fixtures:
            if name == fxt['name']:
                # hit
                url = fxt['url']
                path = fxt['path']
                with open(path) as f:
                    content = f.read()
                    return response.html.HtmlResponse(url, body=content, request=request.Request(url), encoding='utf8')
        return None



    
# change default UserAgent
if sys.version_info.major < 3:
    class UAURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36"
    urllib.request._urlopener = UAURLopener()
else:
    import urllib.request
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36")]
    urllib.request.install_opener(opener)


