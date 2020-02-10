from scrapy.cmdline import execute
import os
from handle_data_mysql import handle_data
# 获取当前文件路径
dirpath = os.path.dirname(os.path.abspath(__file__))
#切换到scrapy项目路径下
os.chdir(dirpath[:dirpath.rindex("\\")])
# 启动爬虫,第三个参数为爬虫name
execute(['scrapy','crawl','用户定义的爬虫名'],func=handle_data)
