

#
#  Scrapy's mognodb 's piple
#
#  Here is the plan,
#  1, each item type  is mapped to a collection. collection name come from item's class.
#  2, each item is a record of the collection above. with new generated id. and a 'key' property, whose value is unique for every scrapped item. the item class should provide that.(or the record will be conflict)
#
#  Mongodb layout. here are two layout.
#  1, only one fixed database (user specified),	 each collection is named as  'project_name +  item type'
#  2, database name is mapped to project name directly. and the collection name is mapped to item type.
#
#

import datetime

from pymongo import MongoClient


class MongoItemMixin(object):
	pass


class MongoItem(Item, MongoItemMixin):
	pass


default_settings = {
	'MONGO_PIPELINE_HOST':'localhost',
	'MONGO_PIPELINE_DBNAME':'scrapy'
}

class MongoPipeline(object):
	def __init__(self, settings):
		self.settings = settings
		self.settings.defaults.update(default_settings)
		self.host = self.settings.get("MONGO_PIPLINE_HOST")
		self.db_name = self.database_name()
		self.client = MongoClient(self.host)
		self.db = self.client[self.db_name]

	def process_item(self, item, spider):
		col = self.db[self.collection_name()]
		key = item['key']
		hit = col.find({ 'key' : key }).count() > 0
		if hit:
			col.insert(dict(item))
		else:
			col.update({'key':key}, dict(item))

	def database_name(self):
		self.settings.get('MONGO_PIPELINE_DBNAME')

	def collection_name(self, item):
		return item.__class__.__name__

	def database_name(self):
		pass
