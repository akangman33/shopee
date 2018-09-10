# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class ShopeePipeline(object):

    def open_spider(self, spider):
        self.con = sqlite3.connect('shopee.sqlite')
        self.cur = self.con.cursor()

    def process_item(self, item, spider):
        insert_sql = "insert into shopee_2 (name, price_min, price_max) values('{}','{}','{}')".format(item['name'], item['price_min'], item['price_max'])
        self.cur.execute(insert_sql)
        # return item

    def close_spider(self, spider):
        self.con.commit()
        self.con.close()
