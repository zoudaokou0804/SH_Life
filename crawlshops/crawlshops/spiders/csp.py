"# -*- encoding:utf-8 -*_",
import os
import sys
import scrapy
# 以下代码解决导入类名报错问题（找不到item类）
fpath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ffpath = os.path.abspath(os.path.join(fpath, ".."))
print(ffpath)
sys.path.append(ffpath)
# from items import CrawlshopsItem

import pandas as pd
import numpy as np
import pymysql
import requests
from lxml import etree
 
dbconn = pymysql.connect(
    host = "localhost",
    database = 'sh_life',
    user = 'root',
    password = '123wangchao'
    )
sql = """SELECT * FROM catalog_index WHERE Classify_First_Level='分类';"""
all_class= pd.read_sql(sql,dbconn)
urllist=all_class.iterrows()
pass

class CspSpider(scrapy.Spider):
    name = 'csp'
    allowed_domains = ['http://www.dianping.com/shanghai/ch10/g1338p1']
    start_urls = ['http://http://www.dianping.com/shanghai/ch10/g1338p1/']

    def parse(self, response):
        pass
