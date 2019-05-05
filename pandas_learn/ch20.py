#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 20 广播
import numpy as np
import pandas as pd

df = pd.DataFrame({'one': pd.Series(np.random.randn(4), index=list('abcd'))})
df['two'] = 1
df['thr'] = 2

print(df)

# 2 从Dataframe中得到一个行和一个列
row = df.iloc[1]
column = df['two']

# print(row, column)

# 3 将df中每一行与row做减法
# print(df.sub(row, axis='columns'))

# 4 广播原理：
# df2 = pd.DataFrame([row for i in range(4)], index=['a', 'b', 'c', 'd'])
# print(df2)
# print(df - df2)

# 5 参数axis指定广播的维度
print(df.sub(row, axis=1))
print(df.sub(column, axis=0))
