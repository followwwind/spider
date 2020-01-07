#!/bin/usr/env python3
# -*- coding: utf-8 -*-

# 爬取网站资源

__author__ = 'wind'

import urllib.request
import re
import os
import time
from functools import reduce

IMG_TYPE_ARR = ['jpg', 'png', 'ico', 'gif', 'jpeg', 'svg']

# 正则表达式预编译
# 这里涉及到了非贪婪匹配
# ((?:/[a-zA-Z0-9.]*?)*)
# ((?:/[a-zA-Z0-9.]*)*?)
REG_RESOURCE_TYPE = r'(?:href|src|data\-original|data\-src)=["\'](.+?\.(?:js|css|jpg|jpeg|png|gif|svg|ico|ttf|woff2|html))[a-zA-Z0-9\?\=\.]*["\']'

regResouce = re.compile(REG_RESOURCE_TYPE, re.S)


# "" or ''
# ?: 取消分组
# ?表示懒惰匹配，尽可能匹配少的字符
url = 'http://v.bootstrapmb.com/2019/5/m9rs04856/index.html'

domain = url[0:url.rfind("/") + 1]

# SAVE_PATH = os.path.join(os.path.abspath('.'), 'python-spider-downloads')
save_path = os.path.join('C:/Users/wind/Desktop/1')

downloadedList = []

'''
解析URL地址
'''
def parseUrl(url):
    if not url:
        return
    
    try:
        response = urllib.request.urlopen(url)

        if response is None or response.status != 200:
            return

        filename = url.replace(domain, '')
        distPath = save_path + filename
        if not filename.startswith('/'):
            distPath = save_path + '/' +filename
        
        dir = distPath[0:distPath.rfind('/')]
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        if os.path.exists(distPath):
            return 
            
        downloadFile(url, distPath)
        if isHtmlType(url): 
            content = response.read().decode('utf-8')
            print('> 网站内容抓取完毕，内容url：', url)
            # 解析网页内容，获取有效的链接
            contentList = re.split(r'\s+', content)
            resourceList = []
            for line in contentList:
                resList = regResouce.findall(line)
                if resList is not None:
                    resourceList = resourceList + resList

            # 对资源进行分组，从而可以下载特定的资源
            # (jsList, cssList, imgList, htmlList) = splitResourceType(resourceList)
            # print(htmlList)
            # return 
            # 下载资源，要区分目录，不存在的话就创建
            for resourceUrl in resourceList:
                if resourceUrl.startswith('http') and resourceUrl.startswith('https') and not resourceUrl.startswith(domain):
                    break
                
                resUrl = resourceUrl
                if not resourceUrl.startswith('http') or not resourceUrl.startswith('https'):
                    resUrl = domain + resourceUrl
                    if resourceUrl.startswith('/'):
                        resUrl = domain + resourceUrl[1:]
                
                parseUrl(resUrl)
    except Exception as e:
        print('报错了：', e)
        print('url：', url)
    

def isCssType(str):
    return str.lower().endswith('.css')

def isHtmlType(str):
    return str.lower().endswith('.html')


def isJsType(str):
    return str.lower().endswith('.js')


def isImgType(str):
    for ext in IMG_TYPE_ARR:
        if str.endswith('.' + ext):
            return True


def splitResourceType(list):
    jsList = []
    cssList = []
    imgList = []
    htmlList = []

    for s in list:
        if isImgType(s):
            imgList.append(s)
        elif isCssType(s):
            cssList.append(s)
        elif isJsType(s):
            jsList.append(s)
        elif isHtmlType(s):
            htmlList.append(s)
        else:
            print('什么类型也不是，解析资源出错！！！：', s)

    htmlList = set(htmlList)
    return jsList, cssList, imgList, htmlList


'''
下载文件
'''
def downloadFile(srcPath, distPath):
    try:
        response = urllib.request.urlopen(srcPath)
        if response is None or response.status != 200:
            return print('> 请求异常：', srcPath)
        data = response.read()
        f = open(distPath, 'wb')
        f.write(data)
        f.close()
        print('>>>: ' + distPath + '：下载成功')
    except Exception as e:
        print('报错了：', e)


def main():
    print(">>>domain:" + domain)
    parseUrl(url)


if __name__ == '__main__':
    main()
    pass
