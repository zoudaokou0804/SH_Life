#!/user/bin/env python
# -*- encoding:utf-8 -*_
'''
@File:进度条.py
@Time:2020/02/08 02:10:42
@Author:zoudaokou
@Version:1.0
@Contact:wangchao0804@163.com
'''
# 参考 https://www.cnblogs.com/wushank/articles/5070792.html

# 字进度条

# from __future__ import division
 
# import sys,time
# j = '#'
# if __name__ == '__main__':
#   for i in range(1,61):
#     j += '#'
#     sys.stdout.write(str(int((i/60)*100))+'% ||'+j+'->'+"\r")
#     sys.stdout.flush()
#     time.sleep(0.5)
# print

# 参考 https://blog.csdn.net/devcloud/article/details/104158417/
"""
# 方法1
import time
import progressbar
p = progressbar.ProgressBar()
N = 10
# 加上进度,就是将range(N)放到ProgressBar()中
for i in p(range(N)):
    #每次延时0.1S
    time.sleep(0.1)
"""

"""
#方法2
import time
import progressbar  
def custom_len(value):
    # These characters take up more space
    characters = {
        '进': 2,
        '度': 2,
    }
 
    total = 0
    for c in value:
        total += characters.get(c, 1)
 
    return total
bar = progressbar.ProgressBar(
    widgets=[
        '进度: ',
        progressbar.Bar(),
        ' ',
        progressbar.Counter(format='%(value)02d/%(max_value)d'),
    ],
    len_func=custom_len,
)
for i in bar(range(10)):
    time.sleep(0.1)
"""



"""
# 花里胡哨请看这里
from alive_progress import showtime
showtime()
"""

# alive-progress库
def alive_progress_bar(num):
    from alive_progress import alive_bar
    import time
    items = range(num)                  # retrieve your set of items
    with alive_bar(len(items)) as bar:   # declare your expected total
        for item in items:               # iterate as usual
            # process each item
            bar()                        # call after consuming one item
            time.sleep(0.1)
            
if __name__ == "__main__":
    num=10
    alive_progress_bar(num)