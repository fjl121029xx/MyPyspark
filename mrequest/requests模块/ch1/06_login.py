#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import requests

session = requests.sessions()

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}
post_url = "http://www.renren.com/PLogin.do"
post_data = {}
# 获取cookie
session.post(post_url, data=post_data, headers=headers)
# 使用session进行请求登录之后才能访问的地址
r = session.get("http://www", headers=headers)

# 保存页面
with open("renren.html", "w", encoding="utf-8") as f:
    f.write(r.content.decode())
