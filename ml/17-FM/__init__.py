#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

# from __future__ import division
from math import exp
import pandas as pd
import numpy as np
from numpy import *
from random import normalvariate
from datetime import datetime
from sklearn import preprocessing


def load_train_data(data):
    global min_max_scaler
    data = pd.read_csv(data)
    labelMat = data.ix[:, -1] * 2 - 1
    X_train = np.array(data.ix[:, :-1])
    min_max_scaler = preprocessing.MinMaxScaler()
    X_train_minmax = min_max_scaler.fit_transform(X_train)
    return X_train_minmax, labelMat


def laod_test_data(data):
    data = pd.read_csv(data)
    labelMat = data.ix[:, -1] * 2 - 1
    X_test = np.array(data.ix[:, :-1])
    X_tset_minmax = min_max_scaler.transform(X_test)
    return X_tset_minmax, labelMat


def sigmoid(inx):
    return 1. / (1. + exp(-max(min(inx, 10), -10)))


def fm_function(data_matrix, class_labels, k, iter):
    m, n = shape(data_matrix)
    alpha = 0.01
    w = zeros((n, 1))
    w_0 = 0.
    v = normalvariate(0, 0.2) * ones((n, k))
    for it in range(iter):
        print(it)
        for x in range(m):
            inter_1 = data_matrix[x] * v
            inter_2 = multiply(data_matrix[x], data_matrix[x]) * multiply(v, v)
            interaction = sum(multiply(inter_1, inter_1) - inter_2) / 2.
            p = w_0 + data_matrix[x] * w + interaction  #
            loss = sigmoid(class_labels[x] * p[0, 0]) - 1
            w_0 = w_0 - alpha * loss * class_labels[x]
            for i in range(n):
                if data_matrix[x, i] != 0:
                    w[i, 0] = w[i, 0] - alpha * loss * class_labels[x] * data_matrix[x, i]
                    for j in range(k):
                        v[i, j] = v[i, j] - alpha * loss * class_labels[x] * (
                                data_matrix[x, i] * inter_1[0, j] - v[i, j] * data_matrix[x, i] * data_matrix[x, i])

    return w_0, w, v


def assessment(data_matrix, class_labels, w_0, w, v):
    m, n = shape(data_matrix)
    allItem = 0
    error = 0
    result = []
    for x in range(m):
        allItem += 1
        inter_1 = data_matrix[x] * v
        inter_2 = multiply(data_matrix[x], data_matrix[x]) * multiply(v, v)
        interaction = sum(multiply(inter_1, inter_1) - inter_2) / 2.
        p = w_0 + data_matrix[x] * w + interaction
        pre = sigmoid(p[0, 0])
        result.append(pre)
        if pre < 0.5 and class_labels[x] == 1.0:
            error += 1
        elif pre >= 0.5 and class_labels[x] == -1.0:
            error += 1
        else:
            continue
    print(result)
    return float(error) / allItem


if __name__ == '__main__':
    # -------读取数据----------
    trainData = './diabetes.csv'
    testData = './diabetes.csv'
    # ------模型训练----
    dataTrain, labelTrain = load_train_data(trainData)
    dataTest, labelTest = laod_test_data(testData)
    w_0, w, v = fm_function(mat(dataTrain), labelTrain, 15, 100)
