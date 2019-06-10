#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 22 填充缺失值
import numpy as np
import pandas as pd

df = pd.DataFrame(np.random.randn(5, 3), index=list('abcde'), columns=('one', 'two', 'three'))
df.iloc[1, : -1] = np.nan
df.iloc[1:-1, 2] = np.nan
print(df)

# 2 使用0替代缺失值
# print(df.fillna(0))

# 3 使用字符串
# print(df.fillna('missing'))

# 4 使用前一个数据代替
# print(df.fillna(method='pad'))

# 5 使用后一个数据代替
# print(df.fillna(method='bfill'))

# 6 使用平均数
# print(df.fillna(df.mean()))

# 7 选择哪一列进行缺失值的处理
print(df.fillna(df.mean()['one':'two']))
