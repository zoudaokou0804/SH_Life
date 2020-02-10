# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # 这是顺序存储
# import pymysql as pm

# class LifeservicePipeline(object):

#     def __init__(self):
#         self.connect = pm.connect(host='localhost',user='root',passwd='123wangchao',db='sh_life')
#         self.cursor = self.connect.cursor()
#         print('数据连接成功')

#     def process_item(self, item, spider):
#         insert_sql = """ insert into catalog_index (ItemName,Classify_First_Level,Classify_Second_Level,Item_Link) values (%s,%s,%s,%s)"""
#         self.cursor.execute(insert_sql,(item['ItemName'], item['Classify_First_Level'],item['Classify_Second_Level'],item['Item_Link']))
#         self.connect.commit()
#     def clos_spider():
#         self.cursor.close()
#         self.connect.close()


# 这是异步存储
import pymysql 
import pymysql.cursors
from twisted.internet import reactor
from twisted.enterprise import adbapi

# 异步更新操作
class LvyouPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )

        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        """
        query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
        # 添加异常处理
        query.addCallback(self.handle_error)  # 处理异常

    def do_insert(self, cursor, item):
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        insert_sql = """ insert into catalog_index (ItemName,Classify_First_Level,Classify_Second_Level,Item_Link) values (%s,%s,%s,%s)"""
        cursor.execute(insert_sql,(item['ItemName'], item['Classify_First_Level'],item['Classify_Second_Level'],item['Item_Link']))
        
    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print(failure)