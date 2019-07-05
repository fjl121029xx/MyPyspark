#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt


class LogisticRegressionGD(object):
    """
    ADAptive LInear NEuron classifier.
    Parameters
    ------------
    eta : float #学习率
      Learning rate (between 0.0 and 1.0)
    n_iter : int  #迭代次数
      Passes over the training dataset.
    random_state : int  #随机数生成器参数
      Random number generator seed for random weight initialization.
    Attributes
    -----------
    w_ : 1d-array #权重
      Weights after fitting.
    cost_ : list #平方误差
      Sum-of-squares cost function value in each epoch.
    """

    # 参数初始化
    def __init__(self, eta=0.01, n_iter=50, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state

    # 拟合数据 进行权值更新 计算错误率

    def fit(self, X, y):
        '''
         """ Fit training data.
        Parameters
        ----------
        X : {array-like}, shape = [n_samples, n_features]
          Training vectors, where n_samples is the number of samples and
          n_features is the number of features.

        X：要进行拟合的输入数据集，有n_sample个样本，每个样本有n_feature个特征值
        例如 X = （[1,2,3],[4,5,6]） [1,2,3]为类别+1，[4,5,6]为类别-1

        y : array-like, shape = [n_samples]
          Target values.
        y:输出数据分类，{+1，-1}

        Returns
        -------
        self : object
        """
        '''
        rgen = np.random.RandomState(self.random_state)
        # 将偏置b并入到w矩阵，所以大小为X行数加1       X.shape[1]代表行数，即样本个数
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=1 + X.shape[1])
        self.cost_ = []

        for i in range(self.n_iter):
            # 在这个代码中activation函数可以不用，写上它只是为了代码的通用性，
            # 比如logistic代码中可以更改为sigmod函数
            net_input = self.net_input(X)
            output = self.activation(net_input)
            errors = (y - output)
            # 更新原理见博客 https://mp.csdn.net/postedit/79668201
            self.w_[1:] += self.eta * X.T.dot(errors)
            self.w_[0] += self.eta * errors.sum()

            # 代价函数改为逻辑回归的对数似然函数
            cost = - y.dot(np.log(output)) - ((1 - y).dot(np.log(1 - output)))
            # 平方误差的总和 Sum of Squred Errors
            self.cost_.append(cost)
        return self

        # 净输入  X点乘W

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

        # 在本代码中 activation没有意义  是为了以后logistic中可以用到

    def activation(self, z):
        return 1. / (1. + np.exp(-np.clip(z, -250, 250)))

        # 预测函数

    def predict(self, X):
        return np.where(self.net_input(X) >= 0.0, 1, 0)
