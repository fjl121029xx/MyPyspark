#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# aggregate分组计算
import numpy as np
import pandas as pd

import pandas.util.testing as tm

colors = tm.np.random.choice(['red', 'green'], size=10)
foods = tm.np.random.choice(['eggs', 'ham'], size=10)

index = pd.MultiIndex.from_arrays([colors, foods], names=['color', 'food'])
df = pd.DataFrame(np.random.randn(10, 2), index=index)
df.columns = ['a', 'b']

print(df)

# 2 根据两个索引进行分组
grouped = df.groupby(level=['color', 'food'])
# print('\nnp.sum')
# print(grouped.aggregate(np.sum))
# print(grouped.sum())

# 4 reset_index() 将两个索引转换为列变量
# print(grouped.aggregate(np.sum).reset_index())
# print(grouped.sum().reset_index())

# 5 as_index() 在分组使用达到reset_index
# df.groupby(level=['color', 'food'], as_index=False)

# 6 size 返回各组数据量
print(grouped.size())

# 7 对各组数据进行描述性统计
print(type(grouped))
print(grouped.describe())
