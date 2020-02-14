"# -*- encoding:utf-8 -*_",
import os
import sys
import scrapy
# 以下代码解决导入类名报错问题（找不到item类）
fpath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ffpath = os.path.abspath(os.path.join(fpath, ".."))
print(ffpath)
sys.path.append(ffpath)
from items import LifeserviceItem
from lxml import etree
from tqdm import tqdm
import time

class DzdpDataSpider(scrapy.Spider):
    name = 'DZDP_Data'
    allowed_domains = ['http://www.dianping.com/shanghai']
    start_urls = ['http://www.dianping.com/shopall/1/0']
    cato1=[]
    cato2=[]
    
    def parse(self, response):
        start_time=time.time()
        class1_list=response.xpath('//div[@class="box shopallCate"]')
        pbar1=tqdm(class1_list,desc='一级大类',leave=False,position=3)
        for c1 in pbar1:            
            c1name=c1.xpath('./h2/text()').extract()[0]
            # pbar1.set_description("一级大类 %s" % c1name)
            class2_list=c1.xpath('./dl')

            # d大学及周边数据另外路径
            university_along_list=c1.xpath('//ul[@class="uniList"]//li//a')
            pbar0=tqdm(university_along_list,desc='大学周边',leave=False,position=2)
            for un in pbar0:
                un_name=un.xpath('./text()').extract()[0]
                un_url=un.xpath('./@href').extract()[0].split('//')[1]
                unit=LifeserviceItem()
                unit['ItemName']=un_name
                unit['Classify_First_Level']='大学周边'
                unit['Classify_Second_Level']='----'
                unit['Item_Link']='http://'+un_url
                yield unit

            pbar2=tqdm(class2_list,desc='二级大类',leave=False,position=2)
            for c2 in pbar2:
                c2name=c2.xpath('./dt//text()').extract()[0]
                # pbar2.set_description("二级大类 %s" % c2name)
                item_list=c2.xpath('./dd//li')
                pbar3=tqdm(item_list,desc='具体类别',leave=False,position=1)
                for item in pbar3:
                    itemname=item.xpath('./a/text()').extract()[0]
                    # pbar3.set_description("具体类别 %s" % itemname)
                    itemurl=item.xpath('./a/@href').extract()[0].split('//')[1]
                    it=LifeserviceItem()
                    it['ItemName']=itemname
                    it['Classify_First_Level']=c1name
                    it['Classify_Second_Level']=c2name
                    it['Item_Link']='http://'+itemurl
                    yield it
                    time.sleep(0.01)
        end_time=time.time()
        print('数据解析完成')
        print('总耗时： %s s' %(end_time-start_time))