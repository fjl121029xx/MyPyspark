#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

###
# 实现梯度下降
# https://www.cnblogs.com/focusonepoint/p/6394339.html
###
import numpy as np
from numpy import genfromtxt

dataPath = "./data.csv"
dataSet = genfromtxt(dataPath, delimiter=",")
print(dataSet)


# print(np.ones((3,2)))

def getDate(dateSet):
    m, n = np.shape(dataSet)
    trainDate = np.ones((m, n))
    trainDate[:, :-1] = dataSet[:, :-1]
    trainLabel = dataSet[:, -1]
    return trainDate, trainLabel


def predict(x, theta):
    m, n = np.shape(x)
    xTest = np.ones((m, n + 1))
    xTest[:, :-1] = x
    yPre = np.dot(xTest, theta)
    return yPre


def batchGradientDescent(x, y, theta, alpha, m, maxIteration):
    xTrains = x.transpose()
    for i in range(0, maxIteration):
        hypothesis = np.dot(x, theta)
        loss = hypothesis - y
        #
        gradient = np.dot(xTrains, loss) / m
        theta = theta - alpha * gradient
    return theta


trainDate, trainLabel = getDate(dataSet)
m, n = np.shape(trainDate)

theta = np.ones(n)
alpha = 0.05
maxIteration = 1000

theta = batchGradientDescent(trainDate, trainLabel, theta, alpha, m, maxIteration)
x = np.array([[3.1, 5.5], [3.3, 5.9], [3.5, 6.3], [3.7, 6.7], [3.9, 7.1]])

print(predict(x, theta))
