#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import requests

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}
kw = {'wd': '斗鱼'}
response = requests.get("http://www.baidu.com/s", headers=headers, params=kw)

# print(response.status_code)
# 判断请求是否成功
assert response.status_code == 200
# 响应头
# print(response.headers)
# 请求头
# print(response.request.headers)
# 内容
# print(response.content.decode())

# example1  实现任意贴吧的爬虫，保存网页到本地

url = 'https://tieba.baidu.com/f?kw=斗鱼tv&ie=utf-8&pn={}'
for i in range(0, 1000, 50):
    response = requests.get(url.format(i))
    print(response.url)
#
