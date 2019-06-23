#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'fjl'

import pandas as pd
import numpy as np
import tensorflow as tf
import operator
from numpy import *
import operator
from os import listdir


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


#
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    # 1 距离计算
    print("---------------------------------------")
    # 建立一个输入向量矩阵
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    print(diffMat)
    print(type(diffMat))
    print("---------------------------------------")
    sqDiffMat = diffMat ** 2
    print(sqDiffMat)
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    print("distances:", distances)
    # argsort 返回数组值从小到大的元素的索引值
    sortedDistIndicies = distances.argsort()
    print("sortedDistIndicies", sortedDistIndicies)

    # 选择距离最小的k个点
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1

    # 排序
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]
