#!/user/bin/env python
# -*- encoding:utf-8 -*_
'''
@File:getshops.py
@Time:2020/02/11 23:15:21
@Author:zoudaokou
@Version:1.0
@Contact:wangchao0804@163.com
'''

import pandas as pd
import numpy as np
import pymysql
import requests
from lxml import etree
from getproxyip import get_proxyip, getheaders
 
dbconn = pymysql.connect(
    host = "localhost",
    database = 'sh_life',
    user = 'root',
    password = '123wangchao'
    )
sql = """SELECT * FROM catalog_index WHERE Classify_First_Level='分类';"""
all_class= pd.read_sql(sql,dbconn)



"""
请求网页返回网页对象
url：网页链接
返回结果：一个通过格式化的html对象
"""
def gethtml(url):
    post_data={'user':'ZoudaokoU_8412','password':'123wangchao'}
    rsp=requests.post(url,data=post_data,allow_redirects=False,headers=getheaders())
    rsp.encoding=rsp.apparent_encoding
    html=etree.HTML(rsp.text)
    return html
"""
获取商店列表页面中单个商店的信息
参数url为单页商铺信息
返回结果为单页的商铺列表

"""
def get_onepage_shops(url):
    ht=gethtml(url)
    shop=ht.xpath('//div[@class="shop-list J_shop-list shop-all-list"]')
    if len(shop)>0:
        shoplist=shop[0].xpath('./ul/li')
        for shop in shoplist:
            name=shop.xpath('./div[@class="txt"]/div[@class="tit"]//@title')[0]
            # comment=
            tag=shop.xpath('./div[@class="txt"]/div[@class="comment"]//text()')
            tagstr=''.join(tag)
            pass
    #         addr=
    #         recommend=
    # else:
    #     pass




"""
解析网页获得点评数量
参数html：为上面返回的格式化的html对象
"""
def get_all_shops(html,url):
    if len(html.xpath('//div[@class="page"]'))>0:
        pages=html.xpath('//div[@class="page"]//a[last()-1]/text()')[0]
    else:
        pages=1
    for i in range(1,int(pages)+1) :
        shops_url=url+'p'+str(i)
        get_onepage_shops(shops_url)




for index,row in all_class.iterrows():
    classname1=row['Classify_Second_Level']
    classname2=row['ItemName']
    classurl=row['Item_Link']
    ht=gethtml(classurl)
    get_all_shops(ht,classurl)

if __name__ == "__main__":
    pass