#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

import pandas as pd
import numpy as np
from pymongo import MongoClient

t = pd.DataFrame(np.arange(12).reshape(3, 4), index=list("abc"), columns=list("qwer"))

d1 = pd.DataFrame({"name": ["xiaoming", "xiaozhang"], "age": [20, 32], "tel": [10086, 10010]})

client = MongoClient(host='', port=27012)
collection = client["douban"]["tv1"]
# data = list(collection.find())

data_list = []
for i in collection.find():
    temp = {}
    temp["info"] = i["info"]
    temp["rating_count"] = i["rating"]["count"]
    temp["rating_value"] = i["rating"]["value"]
    temp["title"] = i["title"]
    temp["country"] = i["tv_category"]
    temp["directors"] = i["directors"]
    temp["actors"] = i["actors"]
    data_list.append(temp)

print(t)
print(d1)

pd.DataFrame(data_list)
