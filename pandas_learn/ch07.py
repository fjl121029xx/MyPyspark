#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'

import numpy as np
import pandas as pd

# pd.set_option('display.mpl_style', 'style')
df = pd.read_csv('../user3000.csv')

# 2 筛选出手机号15的用户
gt15 = df[df[u'reg_phone'] > 15000000000]
print(gt15[:3])

# 4 统计reg_from
counts = gt15[u'reg_from'].value_counts()
print(counts)

# 5 统计总reg_from
counts_all = df[u'reg_from'].value_counts()
print(counts_all)

# 6 计算百分比
per = counts / counts_all
print(per)
