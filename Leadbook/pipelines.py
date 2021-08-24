# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os

import pymongo

#from scrapy.utils.project import get_project_settings as settings
#settings = get_project_settings()



class LeadbookPipeline:
    def open_spider(self, spider):
        self.company_index = open('company_index.json', 'w')
        self.company_profiles = open('company_profiles.json', 'w')
        header='['
        self.company_index.write(header)
        self.company_profiles.write(header)

    def close_spider(self, spider):
        footer=']'
        self.company_index.seek(-2, os.SEEK_END)
        self.company_profiles.truncate()
        self.company_index.write(footer)

        self.company_profiles.seek(-2, os.SEEK_END)
        self.company_profiles.truncate()
        self.company_profiles.write(footer)

        self.company_index.close()
        self.company_profiles.close()

    def process_item(self, item, spider):
        if item['record_type'] == 'company_index':
            line = json.dumps(ItemAdapter(item).asdict()) + ",\n"
            self.company_index.write(line)
            return item
        elif item['record_type'] == 'company_profiles':
            line = json.dumps(ItemAdapter(item).asdict()) + ",\n"
            self.company_profiles.write(line)
            return item

class LeadbookPipeline2:
    def __init__(self):
        self.conn = pymongo.MongoClient(
           "localhost",
            27017
        )
        db = self.conn["Leedbook"]
        self.collection1 = db["company_index"]
        self.collection2 = db["company_profiles"]

    def process_item(self, item, spider):
        if item['record_type'] == 'company_index':
            self.collection1.insert(dict(item))
        elif item['record_type'] == 'company_profiles':
            self.collection2.insert(dict(item))
        return item