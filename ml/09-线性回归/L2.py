#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

import matplotlib.pyplot as plt
from sklearn.datasets import load_boston
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib

"""
    带有正则化的线性回归：岭回归
"""


def ridge():
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

    # 岭回归
    rid = Ridge(alpha=1.0)
    rid.fit(x_train, y_train)

    # 模型保存
    joblib.dump(rid, 'rid.pkl')
    # est = joblib.load('/tmp/rid.pkl')

    #
    print(rid.coef_)
    y_predicted = rid.predict(x_test)
    print(y_predicted)
    print("损失值：",
          mean_squared_error(ss2.inverse_transform(y_predicted), ss2.inverse_transform(y_test)))
    print(ss2.inverse_transform(y_predicted))
    return None


if __name__ == "__main__":
    ridge()
