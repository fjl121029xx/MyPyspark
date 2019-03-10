#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

from sklearn.datasets import load_iris, fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

"""
    小数据集
"""


def iris():
    li = load_iris()
    print("获取特征值")
    print(li.data)
    print("目标值")
    print(li.target)
    print("描述")
    print(li.DESCR)
    #
    x_train, x_test, y_train, y_test = train_test_split(li.data, li.target, test_size=0.25)
    print(x_train)
    print(x_test)
    print(y_train)
    print(y_test)

    return None


"""
    大数据集
"""


def news20():
    n20 = fetch_20newsgroups(subset='all')
    print(n20.data)
    print(n20.target)

    return None


if __name__ == '__main__':
    news20()
