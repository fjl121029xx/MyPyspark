#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# groupby 选择列和迭代
import numpy as np
import pandas as pd

import pandas.util.testing as tm

colors = tm.np.random.choice(['red', 'green'], size=10)
foods = tm.np.random.choice(['eggs', 'ham'], size=10)

index = tm.MultiIndex.from_arrays([colors, foods], names=['color', 'food'])
df = pd.DataFrame(np.random.randn(10, 2), index=index)
df.columns = ['a', 'b']

# print(df)

# 4 以color index进行分类，然后选择a列数据，分组计算求和
# grouped = df.groupby(level='color')
# grouped_a = grouped['a']
# print(grouped_a.sum())

# 5 计算所有lie
# print(grouped.sum())

# 6 迭代输出各组的数据
# for name, group in grouped:
#     print(name)
#     print(group)

# 7 两个索引迭代
grouped = df.groupby(['color', 'food'])
for name, group in grouped:
    print(name)
    print(group)
