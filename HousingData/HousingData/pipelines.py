# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#!/user/bin/env python
# -*- encoding:utf-8 -*_
'''
@File:pipelines.py
@Time:2020/02/08 02:12:20
@Author:zoudaokou
@Version:1.0
@Contact:wangchao0804@163.com
'''

import pymysql as pm


class HousingdataPipeline(object):

    # 以下为同步数据到数据库，单线程
    def __init__(self):
        self.connect = pm.connect(host='localhost',
                                  user='root',
                                  passwd='123wangchao',
                                  db='sh_life')
        self.cursor = self.connect.cursor()
        print('数据连接成功')

    def process_item(self, item, spider):
        insert_sql = """ insert into housingdata (Name,District,BuildYear,BuildingType,PropertyFee,Property_Co,Developers,BuildingsNum,HouseNum,Address,Remarks,FocusNum,AveragePrice,SailNum,Data_HouseCode,Town) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        self.cursor.execute(
            insert_sql,
            (item['Name'], item['District'], item['BuildYear'],
             item['BuildingType'], item['PropertyFee'], item['Property_Co'],
             item['Developers'], item['BuildingsNum'], item['HouseNum'],
             item['Address'], item['Remarks'], item['FocusNum'],
             item['AveragePrice'], item['SailNum'], item['Data_HouseCode'],
             item['Town']))
        self.connect.commit()

    def clos_spider():
        self.cursor.close()
        self.connect.close()
