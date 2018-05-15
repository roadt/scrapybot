

import scrapy

class ItemAssertion:

    def assertItemRequired(self, item, fields=None):
        '''assert fields of item is not none.   

        require can be configured in Item defintion:
           xx = Field(required=True)

       more field to check can  be passed in  fields parameter of this method
        assertItemRequired(item, ['field1', 'field2', 'field3'])
        
        both fields above are checked and must not none. otherwise assertion failed
          
        '''
        if isinstance(item, scrapy.item.Item):
            for n, cfg  in item.fields.iteritems():
                if cfg.get('required'):
                    self.assertIsNotNone(item.get(n), "%s is required but None"%n)
                    
            fields = fields or []
            for n in fields:
                if n in item.fields:
                    self.assertIsNotNone(item.get(n), "%s is required but None"%n)
                else:
                    self.fail("%s is not valid field"%n)