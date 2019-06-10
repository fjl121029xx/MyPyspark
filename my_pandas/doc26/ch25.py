#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 25 插值法填补缺失值
import numpy as np
import pandas as pd

df = pd.DataFrame(np.random.randn(5, 3), index=list('abcde'), columns=['one', 'two', 'thr'])
df.iloc[1, :-1] = np.nan
df.iloc[1:-1, 2] = np.nan
print(df)

# 2 使用插值法估计缺失值
# print(df.interpolate())

# 4 index是数字
# df.index = [1, 2, 4, 5, 6]
# print(df)
# print(df.interpolate(method='values'))

# 5 index是时间
df.index = pd.date_range(20140102, periods=5)
print(df)
print(df.interpolate(method='time'))
