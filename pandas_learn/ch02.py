#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 选择数据
import numpy as np
import pandas as pd

data_index = pd.date_range("2019-04-24", periods=13)
# print(data_index)

df = pd.DataFrame(np.random.randn(13, 4), index=data_index, columns=list("ABCD"))
# print(df)

# 2 选择数据
# print(df['A'])

# 3 数组切片
# print(df[1:4])

# 5 使用行标签指定输出的行
# print(df['2019-04-24':'2019-04-26'])

# 6 loc方法是帮助选择数据的，比如选择索引位置为0的一行数据
# print(df.loc[data_index[0]])

# 7 选择多列数据方法
# print(df.loc[:, ['A', 'B']])

# 8 选择局部数据，是行和列的交叉区域
# print(df.loc['2019-04-24':'2019-04-27', ['A', 'B']])

# 9 只选择某一个数据，可以指定行和列
# print(df.loc[data_index[0], ['A']])

# 10 at方法专门用于获取某个值
print(df.at[data_index[0], 'A'])
