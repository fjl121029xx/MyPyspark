#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

import matplotlib.pyplot as plt
from sklearn.datasets import load_boston
from sklearn.linear_model import SGDRegressor, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

x = []
y = []

plt.figure(figsize=[10, 10])

x = [60, 72, 75, 80, 83, 87, 90, 93]
y = [126, 151.2, 157.5, 168, 174.3, 180, 192.2, 194]

plt.scatter(x, y)

plt.show()


def sgd():
    """
    :return:
    """
    # 获取数据
    lb = load_boston()

    # 分割数据集
    x_train, x_test, y_train, y_test = train_test_split(lb.data, lb.target, test_size=0.25)

    # 标准haul处理
    ss = StandardScaler()
    x_train = ss.fit_transform(x_train)
    x_test = ss.transform(x_test)

    ss2 = StandardScaler()
    y_train = ss2.fit_transform(y_train.reshape(-1, 1))
    y_test = ss2.transform(y_test.reshape(-1, 1))

    # 正规方程
    sgd = SGDRegressor()
    sgd.fit(x_train, y_train)

    print(sgd.coef_)
    y_predicted = sgd.predict(x_test)
    print(y_predicted)
    print("损失值：",
          mean_squared_error(ss2.inverse_transform(y_predicted), ss2.inverse_transform(y_test)))
    print(ss2.inverse_transform(y_predicted))
    return None


def lr():
    """

    :return:
    """
    # 获取数据
    lb = load_boston()

    # 分割数据集
    x_train, x_test, y_train, y_test = train_test_split(lb.data, lb.target, test_size=0.25)

    # 标准haul处理
    ss = StandardScaler()
    x_train = ss.fit_transform(x_train)
    x_test = ss.transform(x_test)

    ss2 = StandardScaler()
    y_train = ss2.fit_transform(y_train.reshape(-1, 1))
    y_test = ss2.transform(y_test.reshape(-1, 1))

    # 正规方程
    lr = LinearRegression()
    lr.fit(x_train, y_train)

    print(lr.coef_)
    print(lr.predict(x_test))
    # print("损失值："lr.)
    print(ss2.inverse_transform(lr.predict(x_test)))
    return None


if __name__ == '__main__':
    sgd()
