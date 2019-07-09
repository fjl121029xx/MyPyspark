#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

ser1 = pd.Series([1, 2, 3, 4, 5])
ser2 = pd.Series([4, 5, 6, 7, 8])

# print(ser1.isin(ser2))
# print(ser2[~ser1.isin(ser2)])

# 取出非公有的数据
ser_u = pd.Series(np.union1d(ser1, ser2))
ser_i = pd.Series(np.intersect1d(ser1, ser2))
# print(ser_u[~ser_u.isin(ser_i)])

# 定位最大、最小、中值
state = np.random.RandomState(seed=100)
ser = pd.Series(state.normal(10, 5, 25))
# print(np.percentile(ser, q=[0, 50, 100]))

# 统计Series中元素出现的个数
ser = pd.Series(np.take(list('abcdefgh'), np.random.randint(8, size=20)))
# print(ser.value_counts())

# 保留Series中出现最多的两个值，其他的值删除掉
ser = pd.Series(np.random.randint(1, 5, 12))
ser[~ser.isin(ser.value_counts().index[:2])] = np.nan
ser = ser.dropna()
print(ser.reindex())

# https://www.jianshu.com/p/be235f6907ca