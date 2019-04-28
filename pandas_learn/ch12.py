#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# transformtion标准
import numpy as np
import pandas as pd

index = pd.date_range('1/1/2014', periods=100)
ts = pd.Series(np.random.normal(0.5, 2, 100), index=index)
print(ts.head())

# 3 lambda函数
key = lambda x: x.month
zscore = lambda x: (x - x.mean()) / x.std()
transformed = ts.groupby(key).transform(zscore)

print(type(transformed))

# 5 先按照月分组数据，然后再计算标准差和平均数
print(transformed.groupby(key).mean())
print(transformed.groupby(key).std())
