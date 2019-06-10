#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 14 按月分组
import numpy as np
import pandas as pd

index = pd.date_range('1/1/2014', periods=100)
ts = pd.Series(np.random.normal(0.5, 2, 100), index)
# print(ts.head())

# 3 假如索引为日期，按月分组
key = lambda x: x.month
grouped = ts.groupby(key)

# print(grouped.first())
# for name, group in grouped:
#     print(name)
#     print(group)

# 4 索引不是日期，但是有一列是日期

date = pd.date_range('1/1/2014', periods=100)
data = np.random.normal(0.5, 2, 100)
df = pd.DataFrame({'date': date, 'data': data})
# print(df.groupby(df['date'].apply(lambda x: x.month)).first())

# 5 可以将日期数据设置为索引
df = df.set_index('date')
# print(df.head())

grouped = df.groupby(key)
# print(grouped.first())

# 6 日期数据是字符串
date_stngs = ('2008-12-20', '2008-12-21', '2008-12-22', '2008-12-23')
a = pd.Series([pd.to_datetime(d) for d in date_stngs])
print(a.head())
