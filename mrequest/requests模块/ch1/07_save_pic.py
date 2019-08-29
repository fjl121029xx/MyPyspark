#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'

import numpy as np
import pandas as pd

import requests

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}

res = requests.get('http://www.baidu.com/img/bd_logo1.png')
assert res.status_code == 200

# print(res.content)

with open('a.png', 'wb') as f:
    f.write(res.content)
