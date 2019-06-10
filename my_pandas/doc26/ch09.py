#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# MultiIndex用法
# https://blog.csdn.net/hnanxihotmail/article/details/81738963
import numpy as np
import pandas as pd

import pandas.util.testing as tm

colors = tm.np.random.choice(['red', 'green'], size=10)
foods = tm.np.random.choice(['eggs', 'ham'], size=10)
print(colors)
print(foods)

# 4 创建MultiIndex对象，然后创建DataFrame
index = pd.MultiIndex.from_arrays([colors, foods], names=['color', 'food'])
df = pd.DataFrame(np.random.randn(10, 2), index=index)
print(df)
#
# print(df.index)

# 5 利用索引获取数据
# print(df.query('color=="red"'))
# print(df.query('food=="ham"'))

# 6 分组使用索引
grouped = df.groupby(level='color')
print(grouped.sum())

# 7 删除或者更改索引的名称,只能用ilevel_0表示第一个索引
df.index.names = [None, None]
# print(df.query('ilevel_0=="red"'))

# 8 分组中，删除掉索引后，只能使用数字1表示第二个索引
grouped = df.groupby(level=0)
print(grouped.sum())
