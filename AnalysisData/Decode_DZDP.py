#!/user/bin/env python
# -*- encoding:utf-8 -*_
'''
@File:get_allcss_link.py
@Time:2020/02/16 00:34:29
@Author:zoudaokou
@Version:1.0
@Contact:wangchao0804@163.com
@desc:大众点评字体加密库解密
'''

# 数据库中去除所有的链接，之前抓取过所有分类的链接，正好用上
import pandas as pd
import numpy as np
import pymysql
import requests
from lxml import etree
from get_proxy_ip import get_proxyip, getheaders
from tqdm import tqdm
# 随机生成请求头
from fake_useragent import UserAgent
import re
from fontTools.ttLib import TTFont  # 解析woff文件
import re
import random
import os

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
        'http://www.dianping.com/shanghai',
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
    return html


"""
函数功能实现遍历所有已有的链接，得到所有css链接，方便后边的到后面字体文件
"""


def getcsslink(url):
    css_list = []
    ht = gethtml(url)
    csslink = ht.xpath("//link[starts-with(@href,'//s3plus')]/@href")
    if len(csslink) > 0:
        css_list.append('http:' + csslink[0])
    else:
        pass
    cssset = list(set(css_list))
    # """
    # 这里写入到txt文件中，主要是为了下面方便调试调用，不用网上再跑一圈数据，节省时间，也免得ip被封
    # """
    # with open(r'C:\Users\a6540\Desktop\大众点评字体加密库\csslink.txt','a', encoding='utf-8') as f1:
    #     for css in cssset:
    #         f1.write(css+'\n')


    # print(cssset)
    return cssset


# getcsslink()
"""不要问我为什么多此一举要在txt中读取css链接，不断调试，心疼我的ip被封"""


def getfontslink(url):
    # 方法2 直接调用上面函数返回结果，这里要从txt中地区主要是为了方便调试，免得再跑一圈网上数据，省的ip又被封了
    li = getcsslink(url)
    # 下面方法熊txt中读取css链接
    # li=[]
    # with open(r'C:\Users\a6540\Desktop\大众点评字体加密库\csslink.txt','r',encoding='utf-8') as f2:
    #     for line in f2:
    #         li.append(line.replace('\n', ''))

    
    # print('\n' + 'css链接集合：')
    # print(li)
    for css in set(li):
        txt = requests.get(css).text
        # print(txt)
        pattern = re.compile('{(.*?)}')
        a = pattern.findall(txt)
        tk = {}  # 新建一个变签名和字体库对应字典
        i = 0
        while i < len(a):
            fonturl = 'http:' + a[i].split('("')[1].split('")')[0]
            tagname = a[i + 1].split('-')[-1][:-2]
            tk[tagname] = fonturl
            i += 2
        # print('\n' + '字体文件链接集合：')
        # print(tk)
        return tk


"""
删除当前文件夹中已经存在的woff和eot文件
"""


def remove_existfile():
    path = os.path.dirname(__file__)
    filenames = os.listdir(path)
    for file in filenames:
        if file.endswith(('eot', 'woff')):
            os.remove(os.path.join(path, file))
    # print(filenames)


# getfonts()
"""根据字体文件链接下载字体文件"""


def loadfonts(url):
    remove_existfile()  # 先删除已经存在的文件
    linklist = getfontslink(url)
    # pbar2 = tqdm(linklist.values(), desc='所有Fonts文件 ', leave=True)
    fontsfile_dict = {}
    for tag, font in linklist.items():
        name = font.split('/')[-1]
        # 当前目录
        pathroot = os.path.dirname(__file__)  # 当前文件夹路径
        path1 = os.path.join(pathroot, name)  # eot文件
        path2 = os.path.join(pathroot, name.replace('eot', 'woff'))  # woff文件
        with open(path1, 'wb') as writer:
            writer.write(requests.get(font).content)
        with open(path2, 'wb') as writer2:
            writer2.write(requests.get(font.replace('eot', 'woff')).content)
            # if 'eot' in name:
            fontsfile_dict[tag] = name
        # else:
        #     pass
    return fontsfile_dict


"""
下载的文字文件手动或识别的文字按顺序组成列表，后面作为字典的值
和字符编码进行zip组合
"""


def get_fonts_values():
    # 先读取txt中字典形成字符串，再转为列表，后面组合字电泳
    pathroot = os.path.dirname(__file__)  # 当前文件夹路径
    path1 = os.path.join(pathroot, '字体.txt')  # eot文件
    with open(path1, 'r', encoding='utf-8') as f3:
        str = f3.read().strip().replace('\n', '')
    values_list = list(str)
    # print(values_list)
    return values_list


"""
采用TTFont解析woff字符文件，得到所有文字的编号
"""


def get_fonts_keys(url):
    files = loadfonts(url)
    for i in files.keys():
        files[i] = files[i].replace('.eot', '.woff')
    # files = [files[fi].replace('.eot', '.woff') for fi in files.keys()]
    kll = {}
    for tag, fi in files.items():
        path = os.path.join(os.path.dirname(__file__), fi)
        font = TTFont(path)
        keys_list = font.getGlyphOrder()[2:]  # 前两个文字为多余的，删除，看百度字体解析导入文件就知道了
        # print(keys_list)
        #########################################
        keys_list = [x + ';'
                     for x in keys_list]  # 添加';'结尾，主要由于网页源码中每个编码后面都跟了一个分好
        ########################################
        kll[tag] = keys_list
    return kll


"""
将前面得到的文字编号列表，和文字组合成
"""


def compile_dict(url):
    dict_list = {}
    kll = get_fonts_keys(url)
    # print(type(keys[1]))
    for tag, keys in kll.items():
        keys2 = [key.replace('uni', '&#x') for key in keys]
        values = get_fonts_values()
        font_dict = dict(zip(keys2, values))
        # print(font_dict)
        dict_list[tag] = font_dict
    return dict_list


"""
解析网页，返还网页源代码，string格式
"""


def get_html_txt(url):
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
    html = rsp.text
    if rsp.status_code == 200:
        return html
    else:
        gethtml(url)


"""
解析查找html源码中的加密编码，输出列表
"""


def get_html_bianma(html):
    pat = re.compile('&#x....;')
    li = pat.findall(html)
    return li


"""
利用list中的函数count,获取每个元素的出现次数
"""


def chongfu_key_count(list1):
    result = {}
    for i in set(list1):
        result[i] = list1.count(i)
    return result

"""
测试专用
直接读取网页源码进行替换操作
主要是防止调试过多被封ip
"""


def changehtml_bysourcecode(url):
    # with open(
    #         r'C:\Users\a6540\Desktop\大众点评字体解密\Decode_DZDP\htmlsourcecode.html',
    #         'r',
    #         encoding='utf-8') as f:
    #     htl = f.read()
    htl = get_html_txt(url)
    dicts = compile_dict(url)
    for tag, dic in dicts.items():
        pat = re.compile('<svgmtsi class="%s">&#x....;</svgmtsi>' % tag)
        ll = pat.findall(htl)
        for x in ll:
            bianma = x.split('">')[1].split('</')[0]
            htl = htl.replace(x, x.replace(bianma, dic[bianma]))
    # with open(
    #         r'C:\Users\a6540\Desktop\大众点评字体解密\Decode_DZDP\htmlsourcecode2.html',
    #         'w',
    #         encoding='utf-8') as f2:
    #     f2.write(htl)
    return htl


# """
# 解析下载下载来的woff文字文件，得到xml文档，
# 后面用来生成字库字典{"字符编码":"对应文字"}
# 这里暂时没用
# """
# def parser_woff():
#     # 注意这里的woff文件其实是上面eot文件是一样的，可以相互转换，在前面下载字体文件的时候可以将其保存下来
#     font = TTFont('test\af3ce6b9.woff')
#     # 将 woff 写为 xml 文件从而就可以对 xml 文件进行操作了
#     font.saveXML('af3ce6b9.xml')

if __name__ == "__main__":
    url = 'http://www.dianping.com/shanghai/ch10/g1338p1'
    # tt = changehtml(url)
    tt = changehtml_bysourcecode(url)
    pat = re.compile('&#x....;')
    li = pat.findall(tt)
    print(li)
