#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 切片操作 iloc像操作数组一样操作DataFrame
import numpy as np
import pandas as pd

data_index = pd.date_range("2019-04-24", periods=6)

df = pd.DataFrame(np.random.randn(6, 4), index=data_index, columns=list("ABCD"))
print(df)

# 2 iloc,提取第四行shuju
# print(df.iloc[3])

# 3 iloc返回值类型
# print(type(df.iloc[1]))

# 4 返回4-5行，1-2列数据
# print(df.iloc[3:5, 1:2])

# 5 提取不连续行和列的数
# print(df.iloc[[1, 2, 4], [0, 2]])

# 6 提取某几行的数据，保证所有列都在
# print(df.iloc[[1, 2, 4], :])

# 7 所有行
# print(df.iloc[:, [2, 3]])

# 8 提取某一个值
# print(df.iloc[0, 0])

# 9 iat 提取某个数，效率高
print(df.iat[0, 0])
