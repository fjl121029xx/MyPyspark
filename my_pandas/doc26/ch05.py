#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'

import numpy as np
import pandas as pd
# 获取当前工作目录
import os

# 2 read_csv 读取csv文件，相对路径
df = pd.read_csv('../user3000.csv', encoding='gbk')
print(df)
print(type(df))
# 3 获取当前工作目录
# print(os.getcwd())

# 4 读取前三行数据
print(df[:3, [2, 3, 4]])
