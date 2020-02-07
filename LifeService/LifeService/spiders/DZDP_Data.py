"# -*- encoding:utf-8 -*_",
import os
import sys
import scrapy
# 以下代码解决导入类名报错问题（找不到item类）
fpath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ffpath = os.path.abspath(os.path.join(fpath, ".."))
print(ffpath)
sys.path.append(ffpath)
from Lifeservice.items import "items文件中Item类名"


class DzdpDataSpider(scrapy.Spider):
    name = 'DZDP_Data'
    allowed_domains = ['http://www.dianping.com/shanghai']
    start_urls = ['http://www.dianping.com/shopall/1/0']

    def parse(self, response):
        pass
