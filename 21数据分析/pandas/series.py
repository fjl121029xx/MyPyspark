#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

from pymongo import MongoClient
import pandas as pd

t = pd.Series([1, 2, 31, 12, 3, 4])
t2 = pd.Series([1, 23, 2, 2, 1], index=list("abcde"))

type(t)

df = pd.read_csv('u.genre')
print(df)
client = MongoClient(host='', port=27012)
collection = client["douban"]["tv1"]
data = list(collection.find())
