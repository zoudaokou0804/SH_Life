# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql as pm

class LifeservicePipeline(object):
    def __init__(self):
        self.connect = pm.connect(host='localhost',user='root',passwd='123wangchao',db='eastmoney_funddata')
        self.cursor = self.connect.cursor()
        print('数据连接成功')

    def process_item(self, item, spider):
        insert_sql = """ insert into table_name (field1,field2,field3) values (%s,%s,%s)"""
        self.cursor.execute(insert_sql,(item['field1'], item['field2'],item['field3']))
        self.connect.commit()
    def clos_spider():
        self.cursor.close()
        self.connect.close()
		
    #def process_item(self, item, spider):
        #return item
