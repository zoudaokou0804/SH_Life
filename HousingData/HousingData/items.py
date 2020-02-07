# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

#!/user/bin/env python
# -*- encoding:utf-8 -*_
'''
@File:items.py
@Time:2020/02/08 02:12:07
@Author:zoudaokou
@Version:1.0
@Contact:wangchao0804@163.com
'''

import scrapy


class HousingdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Name = scrapy.Field() # 小区名称
    District = scrapy.Field() # 所属行政区
    BuildYear = scrapy.Field() # 建筑年代
    BuildingType = scrapy.Field() # 建筑类型
    PropertyFee = scrapy.Field() # 物业费用
    Property_Co = scrapy.Field() # 物业公司
    Developers = scrapy.Field() # 开发商
    BuildingsNum = scrapy.Field() # 楼栋总数
    HouseNum = scrapy.Field() # 房屋总数
    Address = scrapy.Field() # 地址
    Remarks = scrapy.Field() # 备注
    FocusNum = scrapy.Field() # 关注用户数
    AveragePrice = scrapy.Field() # 挂牌均价
    SailNum = scrapy.Field() # 在售二手房套数
    Data_HouseCode = scrapy.Field() # 小区编码
    Town = scrapy.Field() # 区下面具体镇
