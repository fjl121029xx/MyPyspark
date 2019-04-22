#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import requests

proxies = {"http": "http://175.175.216.47:1133"}
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}

response = requests.get("http://www.baidu.com", proxies=proxies, headers=headers)
print(response.status_code)
