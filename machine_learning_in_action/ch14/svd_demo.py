#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy
import tensorflow as tf
import svdRec
from numpy import *

# U, sigma, VT = linalg.svd([[1, 1], [7, 7]])
# print(U)
# print(sigma)
# print(VT)
# 原始矩阵
data = svdRec.load_ex_data()
# print(data)
U, sigma, VT = linalg.svd(data)
# print('------U------')
# print(U)
# print('------sigma------')
# print(sigma)
# print('------VT------')
# print(VT)

# 用svd奇异值重构原始矩阵
sig3 = mat([
    [sigma[0], 0, 0],
    [0, sigma[1], 0],
    [0, 0, sigma[2]]
])

newData = U[:, :3] * sig3 * VT[:3, :]
# print('------newData------')
# print(newData)

# 14-1 相似度计算
mymat = mat(data)
# eusim2 = calSim.euclidSim(mymat[:, 0], mymat[:, 2])
# eusim4 = calSim.euclidSim(mymat[:, 0], mymat[:, 4])
# print(eusim2)
# print(eusim4)

# pearsim2 = calSim.pearsSim(mymat[:, 0], mymat[:, 2])
# print(pearsim2)
# pearsim4 = calSim.pearsSim(mymat[:, 0], mymat[:, 4])
# print(pearsim4)

# cossim2 = calSim.cosSim(mymat[:, 0], mymat[:, 2])
# print(cossim2)
# cossim4 = calSim.cosSim(mymat[:, 0], mymat[:, 4])
# print(cossim4)

# svd 推荐系统
# mymat[0, 1] = mymat[0, 0] = mymat[1, 0] = mymat[2, 0] = 4
# mymat[3, 3] = 2
# my_mat = mat(svdRec.load_ex_data2())
# print(svdRec.recommend(my_mat, 2))


U, sigma, VT = linalg.svd(mat(svdRec.load_ex_data_big()))
print(sigma)
# 总能量
sig2 = sigma ** 2
print(sum(sig2))
print(sum(sig2) * 0.9)
print(sum(sig2[:4]))
