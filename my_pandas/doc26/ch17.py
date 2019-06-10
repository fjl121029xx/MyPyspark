#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 17 字符串提取数据
import numpy as np
import pandas as pd

s = pd.Series(['a1', 'a2', 'b1', 'b2', 'c3', 'c'])
print(s)

# 2 extrct 提取数字
# print(s.str.extract('[ab](\d)'))

# 3 提取多个数据
# print(s.str.extract('[abc](\d)'))

# 4 问号？
# print(s.str.extract('([abc])(\d)?'))

# 5 输出的结果包含变量名.
print(s.str.extract('(?P<letter>[abc])(?P<digit>\d)'))
