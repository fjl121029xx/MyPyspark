# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 16 字符串替换
import numpy as np
import pandas as pd

s = pd.Series(list('ABCDEF'))
# print(s)

# 2 转化为小写
print(s.str.lower())

# 3 大写
# print(s.str.upper())

# 4 获取长度
# print(s.str.len())

# 5 切割字符串
s2 = pd.Series(['a_b_c', 'c_a_b', np.nan, 'f_g_n'])
# print(s2.str.split("_"))
# print(type(s2.str.split("_")))

# 6 如果list构成的数据列比较怪，我们可以使用get方法获得列中的某个
# print(s2.str.split("_").str.get(1))
# print(s2.str.split("_").str[1])

# 7 替换
print(s2.str.replace('^a|b$', 'X', case=False))
