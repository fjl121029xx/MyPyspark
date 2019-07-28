#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 筛选数据
import numpy as np
import pandas as pd

df = pd.DataFrame(np.random.randn(6, 4), columns=list('ABCD'))

print(df)

# 2 选择3列数据大于0的
# print(df[df.D > 0])

# 3 使用&符号可实现多条件筛选
# print(df[(df.D > 0) & (df.C > 0.3)])
# print(df[(df.D > 0) | (df.C > 0.3)])

# 4 在筛选条件下，只返回几个列
# print(df[['A', 'B']][(df.D > 0) & (df.C > 0.3)])

# 5 筛选条件通过一个布尔索引完成
# print(df.D > 0)

# 6 insin筛选特定的值
alist = [0.318735, 0.687075, 0.368485]
print(df['D'].isin(alist))
print(df[df['D'].isin(alist)])
