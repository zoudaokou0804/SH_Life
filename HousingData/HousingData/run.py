#!/user/bin/env python
# -*- encoding:utf-8 -*_
'''
@File:run.py
@Time:2020/02/08 02:11:50
@Author:zoudaokou
@Version:1.0
@Contact:wangchao0804@163.com
'''

from scrapy.cmdline import execute
import os
from Handle import handle_data
# 获取当前文件路径
dirpath = os.path.dirname(os.path.abspath(__file__))
#切换到scrapy项目路径下
os.chdir(dirpath[:dirpath.rindex("\\")])
# 启动爬虫,第三个参数为爬虫name
execute(['scrapy','crawl','LianJia'],func=handle_data)