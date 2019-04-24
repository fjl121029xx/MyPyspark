#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# DataFrame入门
#  1 导入
import numpy as np
import pandas as pd

# 2 创建时间索引
print('\n2 创建时间索引')
dates = pd.date_range('20190419', periods=6)
print(dates)

# 3 创建6*4数据
print('\n3 创建6*4数据')
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
print(df)

# 4 创建一个列名为A的数据框
print('\n4 创建一个列名为A的数据框')
df2 = pd.DataFrame({'A': np.random.randn(6), })
print(df2)

# 5 字典创建DATAFrame
print('\n5 字典创建DATAFrame')
df3 = pd.DataFrame({'A': pd.Timestamp('20190419'),
                    'B': pd.Series(1),
                    })
print(df3)

# 6 加入字典内的数据长度不同，以最长的数据为准
print('\n6 加入字典内的数据长度不同，以最长的数据为准')
df4 = pd.DataFrame({'A': pd.Timestamp('20190419'),
                    'B': pd.Series(1, index=list(range(4))),
                    })
print(df4)

# 7 查看各行数据格式
print('\n7 查看各行数据格式')
print(df4.dtypes)

# 8 查看所有数据
print('\n8 查看所有数据')
print(df)

# 10 查看前三行数据
print('\n10 查看前三行数据')
print(df.head(3))

# 11 tail查看后2行数据
print('\n11 tail查看后2行数据')
print(df.tail(2))

# 12 查看数据框的索引
print('\n12 查看数据框的索引')
print(df.index)

# 13 查看列名用
print('\n13 查看列名用')
print(df.columns)

# 14 查看数据值
print('\n14 查看数据值')
print(df.values)

# 15 查看描述性统计
print('\n15 查看描述性统计')
print(df.describe())

# 16 使用type看一下输出的描述性统计是什么样的数据类型
print('\n16 使用type看一下输出的描述性统计是什么样的数据类型')
print(type(df.describe()))

# 17 使用T来转置
print('\n17 使用T来转置')
print(df.T)

# 18 对数据进行排序，可以指定根据哪一列数据进行排序
print('\n18 对数据进行排序，可以指定根据哪一列数据进行排序')
print(df.sort_values('D', inplace=False))
