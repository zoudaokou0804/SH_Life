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
from get_proxy_ip import get_proxyip, getheaders
from fake_useragent import UserAgent
from tqdm import tqdm
from shopclass import meishi_ShopItem
import pymysql as pm
from Decode_DZDP import changehtml_bysourcecode
import time
"""
读取之前爬取的大众点评所有分类总页面的链接
http://www.dianping.com/shopall/1/0
"""


def get_all_link():
    dbconn = pymysql.connect(host="localhost",
                             database='sh_life',
                             user='root',
                             password='123wangchao')
    Classify_First_Level = '分类'
    Classify_Second = '美食'
    sql = """SELECT * FROM catalog_index WHERE Classify_First_Level='%s';""" % Classify_First_Level
    class_links = pd.read_sql(sql, dbconn)
    # all_link = all_class['Item_Link']
    # dbconn.close()
    return class_links


"""
打开数据库
"""


def openmysql():
    connect = pm.connect(host='localhost',
                         user='root',
                         passwd='123wangchao',
                         db='sh_life')
    cursor = connect.cursor()
    return connect, cursor
    print('数据连接成功')


"""
插入数据
"""


def inserttomysql(shopitem):
    connect, cursor = openmysql()
    insert_sql = """ insert into meishi_shopsinfo (name,classname,commentNum,AvPerConsume,tag1,tag2,recommend,kouwei,huanjing,fuwu,shop_info_url,shop_tuangou_utl,shop_id,shop_poi,shop_address,shop_all_comments_link) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(
        insert_sql,
        (shopitem.name, shopitem.classname, shopitem.commentNum,
         shopitem.AvPerConsume, shopitem.tag1, shopitem.tag2,
         shopitem.recommend, shopitem.kouwei, shopitem.huanjing, shopitem.fuwu,
         shopitem.shop_info_url, shopitem.shop_tuangou_utl, shopitem.shop_id,
         shopitem.shop_poi, shopitem.shop_address,
         shopitem.shop_all_comments_link))
    connect.commit()


"""
关闭数据库
"""


def closemysql():
    connect, cursor = openmysql()
    cursor.close()
    connect.close()


"""
请求网页返回网页对象
url：网页链接
返回结果：一个通过格式化的html对象
"""


def gethtml(url):
    data = {
        'cityId': '1',
        'cityChName': '上海',
        'cityEnName': 'shanghai',
        'pageType': 'search',
        'userId': '1142709687',
        'userName': 'ZoudaokoU_8412',
        'searchType': 'category',
        'categoryId': '0',
        'seo': 'false'
    }
    user_agent = UserAgent().random
    headers = {
        'User-Agent':
        user_agent,
        'Referer':
        url,
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Connection':
        'keep-alive',
        'Cookie':
        'navCtgScroll=0; _lxsdk_cuid=1701b0d982b7c-001b7e25110448-3a65420e-1fa400-1701b0d982cc8; _lxsdk=1701b0d982b7c-001b7e25110448-3a65420e-1fa400-1701b0d982cc8; _hc.v=563cf142-fbcb-d930-575f-1b7a8e71987a.1581001842; s_ViewType=10; ua=ZoudaokoU_8412; ctu=72ebc9cb42cc57573729b84348eccf3564be61a380fc3b49751f82ac13a1c08f; aburl=1; cy=1; cye=shanghai; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1581358123,1581402480,1581431820; cityInfo=%7B%22cityId%22%3A1%2C%22cityName%22%3A%22%E4%B8%8A%E6%B5%B7%22%2C%22provinceId%22%3A0%2C%22parentCityId%22%3A0%2C%22cityOrderId%22%3A0%2C%22isActiveCity%22%3Afalse%2C%22cityEnName%22%3A%22shanghai%22%2C%22cityPyName%22%3Anull%2C%22cityAreaCode%22%3Anull%2C%22cityAbbrCode%22%3Anull%2C%22isOverseasCity%22%3Afalse%2C%22isScenery%22%3Afalse%2C%22TuanGouFlag%22%3A0%2C%22cityLevel%22%3A0%2C%22appHotLevel%22%3A0%2C%22gLat%22%3A0%2C%22gLng%22%3A0%2C%22directURL%22%3Anull%2C%22standardEnName%22%3Anull%7D; dplet=c19cde79cace62a3b84ea7fc3b9454c0; dper=a4b4e7fd903b7d0657c3b5fb3d28472c30e24bb340ec9685e34c0817ecdcacb7c0e7ebee2c23a33f4c66c269f130196d87417f9229988fe80655c91e020ee24fb60a07d26486197a2b622256b257bce245743be3fba70a73fa8e67d136d58aa5; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=17046d5304b-b9d-7cf-324%7C%7C92'
    }
    rsp = requests.get(url, params=data, headers=headers)
    rsp.encoding = 'utf-8'
    html = etree.HTML(rsp.text)
    if rsp.status_code == 200:
        return html
    else:
        gethtml(url)
    # if rsp.status_code==200:
    #     if len(html.xpath('//div[@class="not-found"]'))>0:
    #         gethtml(url)
    #     else:
    #         return html
    # else:
    #     gethtml(url)


"""
美食类店铺信息
获取商店列表页面中单个商店的信息
参数url为单页商铺信息
返回结果为单页的商铺列表
"""


def get_meishi_onepage_shops(url, classname):
    ht = etree.HTML(changehtml_bysourcecode(url))
    shop = ht.xpath('//div[@class="shop-list J_shop-list shop-all-list"]')
    if len(shop) > 0:
        shoplist = shop[0].xpath('./ul/li')
        # 以下对商铺信息的解析只针对美食类的店铺，其他类别由于其在网站代码上的标签不一致，没法写通用的，所以只能针对美食类商铺信息爬取
        pbar3 = tqdm(shoplist,
                     desc='每一页%s家店铺信息' % (len(shoplist)),
                     leave=False,
                     position=1)
        for shop in pbar3:
            # shopitem=meishi_ShopItem()
            name = shop.xpath(
                './div[@class="txt"]/div[@class="tit"]//@title')[0]
            # 判断店铺是否有评论数
            if len(
                    shop.xpath(
                        './div[@class="txt"]/div[@class="comment"]/a[1]/b')
            ) > 0:
                commentNum_list = shop.xpath(
                    './div[@class="txt"]/div[@class="comment"]/a[1]//b//text()'
                )
                commentNum = ''.join(commentNum_list).replace('\n', '')
            else:
                commentNum = '0'  # 没有评论设置为默认0条
            # 判断店铺是否有人均消费信心
            if len(
                    shop.xpath(
                        './div[@class="txt"]/div[@class="comment"]/a[2]/b')
            ) > 0:
                AvPerConsume_list = shop.xpath(
                    './div[@class="txt"]/div[@class="comment"]/a[2]//b//text()'
                )
                AvPerConsume = ''.join(AvPerConsume_list[1:]).replace('\n', '')
            else:
                AvPerConsume = '0'
            # 标签1，分类指标
            tag1_list = shop.xpath(
                './div[@class="txt"]/div[@class="tag-addr"]/a[1]//text()')
            tag1 = ''.join(tag1_list)
            # 标签2，区域范围
            tag2_list = shop.xpath(
                './div[@class="txt"]/div[@class="tag-addr"]/a[2]//text()')
            tag2 = ''.join(tag2_list)
            # print(tag2)
            # 推荐菜信息
            if len(shop.xpath(
                    './div[@class="txt"]/div[@class="recommend"]/a')) > 0:
                recommend_list = shop.xpath(
                    './div[@class="txt"]/div[@class="recommend"]//text()')
                recommend = '、'.join((''.join(recommend_list).replace(
                    '\n', '').strip()).split('：')[1].split())
            else:
                recommend = '无推荐菜'
            # 口味，环境 服务评分信息
            if len(
                    shop.xpath(
                        './div[@class="txt"]/span[@class="comment-list"]')
            ) > 0:
                kouwei_list = shop.xpath(
                    './div[@class="txt"]/span[@class="comment-list"]/span[1]//b//text()'
                )  # 口味评分
                kouwei = ''.join(kouwei_list)
                huanjing_list = shop.xpath(
                    './div[@class="txt"]/span[@class="comment-list"]/span[2]//b//text()'
                )  # 环境评分
                huanjing = ''.join(huanjing_list)
                fuwu_list = shop.xpath(
                    './div[@class="txt"]/span[@class="comment-list"]/span[3]//b//text()'
                )  # 服务评分
                fuwu = ''.join(fuwu_list)
            else:
                pass
            # 这里会出现两个链接，第一个链接是商铺详细信息页面链接，另一个是商铺团购页面链接（有可能没有）
            shop_url_list = shop.xpath(
                './div[@class="txt"]/div[@class="tit"]//@href')
            if len(shop_url_list) > 1:
                shop_info_url = shop_url_list[0]  # 商铺详细信息页面链接
                shop_tuangou_utl = shop_url_list[1]  # 商铺团购页面链接
                # shop_waimai_utl=shop_url_list[2] # 商铺外卖页面链接（可能有）
            else:
                shop_info_url = shop_url_list[0]  # 只有商铺详细信息页面链接
                shop_tuangou_utl = '无团购信息'
            # 收藏 地图 附近 标签种隐藏的信息
            otherinfo = shop_address = shop.xpath(
                './div[@class="operate J_operate Hide"]')
            if len(otherinfo) > 0:
                shop_id = shop.xpath(
                    './div[@class="operate J_operate Hide"]/a[1]/@data-shopid'
                )[0]  # 店铺id
                shop_poi = shop.xpath(
                    './div[@class="operate J_operate Hide"]/a[2]/@data-poi')[
                        0]  # 店铺兴趣点
                shop_address = shop.xpath(
                    './div[@class="operate J_operate Hide"]/a[2]/@data-address'
                )[0]  # 店铺地址
                shop_all_comments_link = 'http://www.dianping.com/' + shop_id + '/review_all'  # 商铺所有评论链接地址，后面可以做单独关键词分析用

            else:
                print('无其他信息（收藏、地图、附近)')

            shopitem = meishi_ShopItem(name, classname, commentNum,
                                       AvPerConsume, tag1, tag2, recommend,
                                       kouwei, huanjing, fuwu, shop_info_url,
                                       shop_tuangou_utl, shop_id, shop_poi,
                                       shop_address,
                                       shop_all_comments_link)  # 新建一个商店类的实例
            inserttomysql(shopitem)
            time.sleep(0.1) # 搞慢点。做人要厚道，对人家服务器温柔以待


"""         
获取魔衣分类所有商铺信息
先获取某一分类中商铺有多少页的商铺，再进行每一页获取商铺信息
参数html：为上面返回的格式化的html对象
"""


def get_all_shops(html, url, classname):
    if len(html.xpath('//div[@class="page"]')) > 0:
        pages = html.xpath('//div[@class="page"]//a[last()-1]/text()')[0]
    else:
        pages = 1
    pbar2 = tqdm(range(1,
                       int(pages) + 1),
                 desc='共计%s页店铺信息 ' % (int(pages)),
                 leave=False,
                 position=2)
    for i in pbar2:
        shops_url = url + 'p' + str(i)
        get_meishi_onepage_shops(shops_url, classname)


"""
从数据库中读取所有分类的链接开始获取所有商铺信息
"""


def get_all_shopsinfo():
    i = 0
    all_class_link = get_all_link()
    # classname1 = all_class_link['Classify_Second_Level']
    openmysql()  # 打开数据库
    classname_list = all_class_link['ItemName']
    url_list = all_class_link['Item_Link']
    pbar1 = tqdm(url_list,
                 desc='所有%s店铺信息' % classname_list[i],
                 leave=False,
                 position=3)
    for classurl in pbar1:
        classname = classname_list[i]
        ht = gethtml(classurl)
        get_all_shops(ht, classurl, classname)
        i += 1
    closemysql()  # 关闭数据库


if __name__ == "__main__":
    get_all_shopsinfo()