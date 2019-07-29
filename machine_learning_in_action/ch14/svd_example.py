#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from numpy import *
from numpy import linalg as la


def sigmaPct(simgma, percentage):
    simgma2 = simgma ** 2
    sumsgm2 = sum(simgma2)
    sumsgm3 = 0
    k = 0
    for i in simgma:
        sumsgm3 += i ** 2
        k += 1
        if sumsgm3 >= sumsgm2 * percentage:
            return k


def compressedBySVD(imgMat):
    # singular value decomposition
    U, s, V = la.svd(imgMat)
    # choose top k important singular values (or eigens)
    # print(len(s))
    # k = sigmaPct(s, 0.9)
    # print(k)
    k = len(s)
    Uk = U[:, 0:k]

    Sk = np.diag(s[0:k])
    Vk = V[0:k, :]
    # recover the image
    imgMat_new = Uk * Sk * Vk
    return imgMat_new


# https://blog.csdn.net/Together_CZ/article/details/78252846


'''
    生成随机数
    产生：100行，10列的数据文件
    '''
# matrix = []
# for i in range(100000):
#     tmp_list = []
#     for j in range(10):
#         tmp_list.append(random.randint(1, 100))
#     matrix.append([str(o) for o in tmp_list])

# with open("data.txt", 'w') as f:
#     for one_list in matrix:
#         f.write(','.join(one_list) + '\n')

init_data = [
    [1, 1, 1, 0, 0],
    [2, 2, 2, 0, 0],
    [5, 5, 5, 0, 0],
    [1, 1, 0, 2, 2],
    [0, 0, 0, 3, 3],
    [0, 0, 0, 1, 1],
]
matrix2 = []
for i in range(1000000):
    tmp_list = []
    for j in range(10000):
        tmp_list.append(random.randint(1, 1000))
    matrix2.append([o for o in tmp_list])

with open("data.txt", 'w') as f:
    for one_list in matrix2:
        arr = [str(e) for e in one_list]
        f.write(','.join(arr) + '\n')

comped_data = compressedBySVD(mat(matrix2))
comped_data_list = comped_data.tolist()
with open("data2.txt", 'w') as f:
    for one_list in comped_data_list:
        arr = [str(e) for e in one_list]
        f.write(','.join(arr) + '\n')

# print(comped_data)
