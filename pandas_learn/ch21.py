#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 21 带有缺失值的计算
import numpy as np
import pandas as pd

df = pd.DataFrame(np.random.randn(5, 3), index=list('abcde'), columns=('one', 'two', 'three'))
df.iloc[1, : -1] = np.nan
print(df)

df2 = pd.DataFrame(np.random.randn(5, 3), index=list('abcde'), columns=('one', 'two', 'three'))
print(df2)

# 4 简单运算
# print(df + df2)

# 5 描述性统计
print(df['one'].sum())
