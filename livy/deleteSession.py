#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import requests

headers = {'X-Requested-By': 'livy'}
# 172.20.44.6
# curl -X DELETE -H "Content-Type: application/json" -H "X-Requested-By: user" http://172.20.44.6:8999/sessions//77447
# 192.168.101.39
# res = requests.delete("http://172.26.25.148:8999/sessions/13", headers=headers)
res = requests.delete("http://172.20.44.6:8999/sessions/77681", headers=headers)
# res = requests.delete("http://bi-olap1.sm02:8999/sessions/8966", headers=headers)
print(res.text)
