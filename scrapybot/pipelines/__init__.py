# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapybot.items import *
import MySQLdb

class ScrapybotPipeline(object):
    def __init__(self):
        self.connection = MySQLdb.connect(host='localhost',user='roadt',passwd='pass',db='test')

    def process_item(self, item, spider):
        c= self.connection.cursor()
        if isinstance(item, Article):
            count = c.execute("select * from articles where url = '%s'" % item['url'])
            if count <= 0:
                sql = "insert into articles (title, url, author_name, author_url, char_count, last_update) values ('%s','%s','%s','%s','%s','%s')" % (item['title'], item['url'], item['author_name'], item['author_url'], item['char_count'], item['last_update'])
                c.execute(sql)
                self.connection.commit()        



