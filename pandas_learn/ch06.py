#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 计数统计
import numpy as np
import pandas as pd

df = pd.read_csv('../user3000.csv')

# 3 选择数据
print(df[u'reg_from'])

# 4 value_counts()
counts = df[u'reg_from'].value_counts()
print(counts)

# 5 会做柱形图
plt = counts.plot(kind='bar').get_figure()
plt.savefig("../plot.png")
