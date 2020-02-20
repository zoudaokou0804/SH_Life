#!/user/bin/env python
# -*- encoding:utf-8 -*_
'''
@File:shopclass.py
@Time:2020/02/16 10:28:38
@Author:zoudaokou
@Version:1.0
@Contact:wangchao0804@163.com
@desc:新建一个shop商铺类，将每一个商铺各种信息组成一个实例
'''


# 这是异步存储
import pymysql 
import pymysql.cursors
from twisted.internet import reactor
from twisted.enterprise import adbapi

# 美食类店铺类
class meishi_ShopItem:
    def __init__(self, name, classname, commentNum, AvPerConsume, tag1, tag2, recommend,kouwei,huanjing,fuwu,shop_info_url,shop_tuangou_utl,shop_id,shop_poi,shop_address,shop_all_comments_link):
        self.name = name  # 店铺名称
        self.classname = classname  # 分类名称，如美食
        self.commentNum = commentNum  # 评论数量
        self.AvPerConsume = AvPerConsume  # 人均消费
        self.tag1 = tag1  # 分类标签信息
        self.tag2 = tag2  # 区位信息
        self.recommend = recommend  # 推荐菜名
        self.kouwei = kouwei  # 口味评分
        self.huanjing = huanjing  # 环境评分
        self.fuwu = fuwu  # 服务评分
        self.shop_info_url = shop_info_url  # 店铺详细页链接
        self.shop_tuangou_utl = shop_tuangou_utl  # 店铺团购页链接
        self.shop_id = shop_id  # 店铺id
        self.shop_poi = shop_poi  # 店铺兴趣点，大众点评上数据，不知道有啥用
        self.shop_address = shop_address  # 店铺地址
        self.shop_all_comments_link = shop_all_comments_link  # 店铺地址

    # def openmysql(self):
    #     self.connect = pm.connect(host='localhost',user='root',passwd='123wangchao',db='sh_life')
    #     self.cursor = self.connect.cursor()
    # def inserttomysql(self):
    #     print('数据连接成功')
    #     insert_sql = """ insert into catalog_index (ItemName,Classify_First_Level,Classify_Second_Level,Item_Link) values (%s,%s,%s,%s)"""
    #     self.cursor.execute(insert_sql,(item['ItemName'], item['Classify_First_Level'],item['Classify_Second_Level'],item['Item_Link']))
    #     self.connect.commit()
    # def closemysql(self):
    #     self.cursor.close()
    #     self.connect.close()