#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 26 值替换
import numpy as np
import pandas as pd

ser = pd.Series([0, 1, 2, 3, 4, 5, 1, 2, 3])
# print(ser)

# 2 替换
# print(ser.replace(0, 6))

# 3 列表到列表
# print(ser.replace([0, 1, 2, 3, 4, 5], [5, 4, 3, 2, 1, 0]))

# 4 字典映射
# print(ser.replace({1: 11, 2: 12}))

# 5 DataFrame
df = pd.DataFrame({'a': [0, 11, 22, 3, 4, 2], 'b': [5, 62, 2, 2, 8, 9]})
print(df.replace(2, 20))
