#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 18 匹配字符串
import numpy as np
import pandas as pd

s = pd.Series(['a1', 'A1', 'b1', 'b2', 'c3', 'abd', 'a2c', np.nan, 'a1b'])
print(s)

# 2 检测序列中哪些元素包含一个字母和数字
pattern = r'[a-z][0-9]'
# print(s.str.contains(pattern))

# 3 na参数规定出现NaN数据的时候匹配成True还是False
# print(s[s.str.contains(pattern, na=True)])

# 4 match严格匹配字符串
# print(s.str.match(pattern))
# print(s[s.str.match(pattern, na=True)])

# 5 检查字符串开始字符
# print(s[s.str.startswith('a', na=False)])
# print(s[s.str.contains('^a', na=False)])

# 6 检查字符串结束字符
print(s[s.str.endswith('1', na=False)])
print(s[s.str.contains('1$', na=False)])

print('3' * 3)
