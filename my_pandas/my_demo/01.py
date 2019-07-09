#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

mylist = list('abc')
myarr = np.arange(3)
mydict = dict(zip(mylist, myarr))

# print("list: {}\nmyarr: {}\nmydict: {}\n".format(mylist, myarr, mydict))

# 　Series 是一个类数组的数据结构，同时带有标签（lable）或者说索引（index）。
#  如何通过list，numpy array， dict创建series
ser1 = pd.Series(mylist)
# print(ser1)
ser2 = pd.Series(myarr)
# print(ser2)
ser3 = pd.Series(mydict)
# print(ser3)
# print(ser3['b'])

# 3 把一个Series转换为DataFrame
df = ser3.to_frame()
# print(df)

# 如果想把Series中的index也一起进行转换，可以使用如下操作
# print(ser3.to_frame().reset_index())

# 合并两个Series组成一个DataFrame
ser1 = pd.Series(list('abcedfghijklmnopqrstuvwxyz'))
ser2 = pd.Series(np.arange(26))
# print(pd.concat([ser1, ser2], axis=1))
print(pd.DataFrame({'col1': ser1, 'col2': ser2}))
