#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 移动复制删除列
import numpy as np
import pandas as pd

import pandas.util.testing as tm

colors = tm.np.random.choice(['red', 'green'], size=10)
foods = tm.np.random.choice(['eggs', 'ham'], size=10)

index = pd.MultiIndex.from_arrays([colors, foods], names=['color', 'food'])
df = pd.DataFrame(np.random.randn(10, 2), index=index)
df.columns = ['a', 'b']

print(df)

# 2 增加列
df['c'] = pd.Series(np.random.randn(10), index=df.index)
# print(df)

# 3 插入一列到任意位置
df.insert(2, 'e', df['a'])
# print(df)

# 4 永久删除一列数据
del df['e']
# print(df)

# 5 drop 不改变原有的df中的数据，而是返回另一个dataframe
# df2 = df.drop(['a', 'b'], axis=1)
# print(df2)

# 6 移动列
b = df.pop('b')
df.insert(0, 'b', b)
print(df)
