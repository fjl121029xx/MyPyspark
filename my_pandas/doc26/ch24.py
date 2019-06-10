#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 24 删除缺失值
import numpy as np
import pandas as pd

df = pd.DataFrame(np.random.randn(5, 3), index=list('abcde'), columns=['one', 'two', 'thr'])
df.iloc[1, :-1] = np.nan
df.iloc[1:-1, 2] = np.nan
print(df)

# 3 删除行
# print(df.dropna(axis=0))

# 4 删除列
print(df.dropna(axis=1))
