#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'

import numpy as np
import pandas as pd

import requests

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}
res = requests.get('http://www.baidu.com')

# print(res.cookies)
# print(requests.utils.dict_from_cookiejar(res.cookies))

# 1 编码
url = 'http://www.baidu.com/f?kw=斗鱼'
# print(requests.utils.quote(url))


# 2 请求SSL证书验证
# res2 = requests.get("https://www.12306.cn/mormhweb/", verify=False)
# assert res2.status_code == 200

# 3 设置超时参数
requests.get('', timeout=10)
