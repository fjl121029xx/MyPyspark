#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'
"""
    归一化
    标准化
    缺失值
"""
from sklearn.preprocessing import MinMaxScaler, StandardScaler, Imputer
import numpy as np


def mm():
    """

    :return:
    """

    # mm = MinMaxScaler(feature_range=(2, 3))
    mm = StandardScaler()

    im = Imputer(missing_values='NaN', strategy='mean', axis=0)
    da = im.fit_transform([[1, 2], [np.nan, 3], [7, 6]])
    print(da)

    data = mm.fit_transform([[1, -1, 3],
                             [2, 4, 2],
                             [4, 6, -1]
                             ])
    # data = mm.fit_transform([[90, 2, 10, 40],
    #                          [60, 4, 15, 45],
    #                          [75, 3, 13, 46]
    #                          ])
    print(data)
    return None


if __name__ == '__main__':
    mm()
