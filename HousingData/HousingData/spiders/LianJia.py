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

import time
from tqdm import tqdm


from tqdm import tqdm
import threading

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
        
        par1=tqdm(Districts_url,ascii=False,desc="全上海",disable=False,dynamic_ncols=False,position=4)
        for p1 in par1:
            # par1.set_description("Processing %s" % p1)
            # dis_url=par1.return_description(p1).split('Processing ')[1].split('c:')[0]+'c' # 注意return_des自定义函数
            dis_url=p1
            ht = parse_html(dis_url)
            towns_url = ht.xpath(
                '//div[@data-role="ershoufang"]//div[2]//a/@href')
            towns_url = [header_url + i for i in towns_url]
            
            par2=tqdm(towns_url,ascii=False,desc="全区",disable=False,dynamic_ncols=False,position=3,leave=False)
            for p2 in par2:
                # par2.set_description("Processing %s" % p2)
                # tw_url=par2.return_description(p2).split('Processing ')[1].split('c:')[0]+'c' # 注意return_des自定义函数
                tw_url=p2
                htt = parse_html(tw_url)
                # json.load解析json数据为字典
                Pages =json.loads(htt.xpath('//div[@class="page-box house-lst-page-box"]/@page-data')[0])['totalPage']
                
                par3=tqdm(range(1,Pages+1),ascii=False,desc="全镇",disable=False,dynamic_ncols=False,position=2,leave=False)
                for p3 in par3:
                    # par3.set_description("Processing %s" % p3)
                    # pgn=par3.return_description(p3).split('Processing ')[1].split(':')[0] # 注意return_des自定义函数
                    pgn=p3
                    pg = 'pg' + str(pgn) + '/?'
                    page_url = pg.join(tw_url.split('?'))
                    # page_url = 'https://sh.lianjia.com/xiaoqu/beicai/pg10/?from=rec'# 错误测试页，待注释
                    hhtt=parse_html(page_url)
                    house_list=hhtt.xpath('//li[@class="clear xiaoquListItem"]')
                    # ll=[etree.tostring(house_list[i]) for i in range(len(house_list))]
                    par4=tqdm(house_list,ascii=False,desc="全页",disable=False,dynamic_ncols=False,position=1,leave=False)
                    # initk=0
                    for p4 in par4:
                        # par4.set_description("Processing %s" % p4)
                        # # house=par4.return_description(p4).split('Processing ')[1].split(':')[0] # 注意return_des自定义函数
                        # house=house_list[initk]
                        house=p4
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
                        # 详情页信息板块
                        info_block=house_info.xpath('//div[@class="xiaoquInfo"]')
                        # 判断信息板块是否存在，若存在则进行一下操作，若不存在则进行替他操作
                        if len(info_block)>0:
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
                        else:
                            hi['BuildYear']='1949'                
                            hi['BuildingType']='暂无信息'
                            hi['PropertyFee']='暂无信息'
                            hi['Property_Co']='暂无信息'
                            hi['Developers']='暂无信息'
                            hi['BuildingsNum']='0'
                            hi['HouseNum']='0'
                            hi['Address']='暂无信息'
                            hi['FocusNum']='0' 
                        yield  hi    
                        # initk +=1                                                 