#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy
import tensorflow as tf
from numpy import linalg as la
from numpy import *
from matplotlib import pyplot as plt


# https://zhuanlan.zhihu.com/p/25801478
def loadExData():
    return mat([
        [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
        [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
        [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
        [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
        [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
        [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
        [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
        [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
        [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
        [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]
    ])


def ecludSim(inA, inB):
    return 1.0 / (1.0 + la.norm(inA - inB))


def pearsSim(inA, inB):
    if len(inA) < 3:
        return 1.0

    # 应用公式0.5*value+0.5可以将相关系数矩阵的值域由[-1,1]映射为[0,1]。
    return 0.5 + 0.5 * corrcoef(inA, inB, rowvar=0)[0][1]


def cosSim(inA, inB):
    num = float(inA.T * inB)
    denom = la.norm(inA) * la.norm(inB)
    #
    return 0.5 + 0.5 * (num / denom)


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


def svdEst(dataMat, user, simMeas, item, percentage):
    n = shape(dataMat)[1]
    simTotal = 0.0
    ratSimTotal = 0.0
    u, sigma, vt = la.svd(dataMat)
    k = sigmaPct(sigma, percentage)
    k = 2
    sigmaK = mat(eye(k) * sigma[:k])
    xforedItems = dataMat.T * u[:, :k] * sigmaK.I

    # numpy.savetxt("xforedItems.txt", xforedItems)

    # print(xforedItems)
    for j in range(n):
        userRating = dataMat[user, j]
        if userRating == 0 or j == item:
            continue
        similarity = simMeas(xforedItems[item, :].T, xforedItems[j, :].T)
        simTotal += similarity
        ratSimTotal += similarity * userRating
    if simTotal == 0:
        return 0
    else:
        return ratSimTotal / simTotal


def recommend(dataMat, user, N=5, simMeas=cosSim, estMethod=svdEst, percentage=0.9):
    unratedItems = nonzero(dataMat[user, :].A == 0)[1]
    if len(unratedItems) == 0:
        return 'you rated everything'
    itemScores = []
    for item in unratedItems:
        estimatedScore = estMethod(dataMat, user, simMeas, item, percentage)
        itemScores.append((item, estimatedScore))
    itemScores = sorted(itemScores, key=lambda x: x[1], reverse=True)
    return itemScores[:N]


if __name__ == "__main__":
    testdata = loadExData()
    print(recommend(testdata, 1, N=2, percentage=0.9))
