#!/user/bin/env python
# -*- encoding:utf-8 -*_
'''
@File:LianJia.py
@Time:2020/02/08 02:11:18
@Author:zoudaokou
@Version:1.0
@Contact:wangchao0804@163.com
'''

import os
import sys
import scrapy
# 以下代码解决导入类名报错问题（找不到item类）
fpath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ffpath = os.path.abspath(os.path.join(fpath, ".."))
print(ffpath)
sys.path.append(ffpath)
from HousingData.items import HousingdataItem
import requests
from bs4 import BeautifulSoup
from lxml import etree
import json

from HousingData.ProgressBar import  alive_progress_bar


def parse_html(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
    resp = requests.get(url,headers=headers)
    resp.encoding = resp.apparent_encoding
    html = resp.text
    htree = etree.HTML(html)
    return htree


class LianjiaSpider(scrapy.Spider):
    name = 'LianJia'
    allowed_domains = ['sh.lianjia.com']
    start_urls = ['https://sh.lianjia.com/xiaoqu/?from=rec']  # 链家网二手房数据

    def parse(self, response):
        Districts_url = response.xpath(
            '//div[@data-role="ershoufang"]//a/@href').extract()
        header_url = 'https://sh.lianjia.com'
        Districts_url = [header_url + i for i in Districts_url][:-1] # 删除上海周边的小区数据连接
        alive_progress_bar(len(Districts_url)) # 进度条1
        for dis_url in Districts_url:
            # bf=parse_html(dis_url)
            ht = parse_html(dis_url)
            towns_url = ht.xpath(
                '//div[@data-role="ershoufang"]//div[2]//a/@href')
            towns_url = [header_url + i for i in towns_url]
            alive_progress_bar(len(towns_url)) # 进度条2
            for tw_url in towns_url:
                htt = parse_html(tw_url)
                # json.load解析json数据为字典
                Pages =json.loads(htt.xpath('//div[@class="page-box house-lst-page-box"]/@page-data')[0])['totalPage']
                alive_progress_bar(Pages) # 进度条3
                for page in range(int(Pages)):
                    pg = 'pg' + str(page + 1) + '/?'
                    page_url = pg.join(tw_url.split('?'))
                    hhtt=parse_html(page_url)
                    house_list=hhtt.xpath('//li[@class="clear xiaoquListItem"]')
                    alive_progress_bar(len(house_list)) # 进度条4
                    for house in house_list:
                        hi=HousingdataItem()
                        hi['Data_HouseCode']=house.xpath('@data-housecode')[0]
                        hi['Name']=house.xpath('./div[1]/div[1]/a/text()')[0]
                        info_url=house.xpath('./div[1]/div[1]/a/@href')[0]
                        hi['Town']= house.xpath('./div[1]/div[3]//a[2]/text()')[0]
                        hi['District']= house.xpath('./div[1]/div[3]//a[1]/text()')[0]
                        if len(house.xpath('./div[1]/div[5]/span/text()')) > 0 :
                            hi['Remarks']= house.xpath('./div[1]/div[5]/span/text()')[0]
                        else:
                            hi['Remarks']=" "
                        price=house.xpath('./div[2]/div[1]//span/text()')[0]
                        if price=='暂无':
                            hi['AveragePrice']='0'
                        else:
                            hi['AveragePrice']=house.xpath('./div[2]/div[1]//span/text()')[0]
                        hi['SailNum']=house.xpath('./div[2]/div[2]//span/text()')[0]
                        # 以下解析详情页数据
                        house_info=parse_html(info_url)
                        year=house_info.xpath('//div[@class="xiaoquInfo"]//div[1]/span[2]/text()')[0]
                        if year=='暂无信息 ':
                            hi['BuildYear']='1949'
                        else:
                            hi['BuildYear']=house_info.xpath('//div[@class="xiaoquInfo"]//div[1]/span[2]/text()')[0].split('年')[0]                       
                        hi['BuildingType']=house_info.xpath('//div[@class="xiaoquInfo"]//div[2]/span[2]/text()')[0]
                        hi['PropertyFee']=house_info.xpath('//div[@class="xiaoquInfo"]//div[3]/span[2]/text()')[0]
                        hi['Property_Co']=house_info.xpath('//div[@class="xiaoquInfo"]//div[4]/span[2]/text()')[0]
                        hi['Developers']=house_info.xpath('//div[@class="xiaoquInfo"]//div[5]/span[2]/text()')[0]
                        hi['BuildingsNum']=house_info.xpath('//div[@class="xiaoquInfo"]//div[6]/span[2]/text()')[0].split('栋')[0]
                        hi['HouseNum']=house_info.xpath('//div[@class="xiaoquInfo"]//div[7]/span[2]/text()')[0].split('户')[0]
                        hi['Address']=house_info.xpath('//div[@class="detailDesc"]/text()')[0]
                        hi['FocusNum']=house_info.xpath('//div[@class="detailFollowedNum"]/span/text()')[0]                       
                        yield  hi