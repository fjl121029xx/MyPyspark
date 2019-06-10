#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# agg分组多种计算
import numpy as np
import pandas as pd
import pandas.util.testing as tm

colors = tm.np.random.choice(['red', 'green'], size=10)
foods = tm.np.random.choice(['eggs', 'ham'], size=10)

index = pd.MultiIndex.from_arrays([colors, foods], names=['color', 'food'])
df = pd.DataFrame(np.random.randn(10, 2), index=index)
df.columns = ['a', 'b']

print(df)

# 2 按照颜色将数据分组
grouped = df.groupby(level='color')
print(grouped)

# 3 计算各组数据的总数、平均标准差
# print(grouped.agg([np.sum, np.mean, np.std]))

# 4 只需要对a列数据计算
# print(grouped['a'].agg([np.sum, np.mean, np.std]))

# 5 定制显示的标题
# print(grouped['a'].agg({'SUM sresult': np.sum, 'MEAN result': np.mean}))

# 6 通过lambda匿名函数来进行特殊的计算
# print(grouped['a'].agg({'lambda': lambda x: np.mean(abs(x))}))

# 7 使用字符串作为一个function
print(grouped['a'].agg({'C': 'sum', 'D': 'std'}))
