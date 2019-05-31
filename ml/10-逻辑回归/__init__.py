#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

"""
    http://archive.ics.uci.edu/ml/machine-learning-databases/
"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report


def logi():
    """

    :return:
    """
    column = ['Sample code number', 'Clump Thickness ', 'Uniformity of Cell Size', 'Uniformity of Cell Shape',
              'Marginal Adhesion', 'Single Epithelial Cell Size ', 'Bare Nuclei ',
              'Bland Chromatin', 'Normal Nucleoli', 'Mitoses', 'Class']
    data = pd.read_csv(
        'http://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data',
        names=column)
    print(data)

    # 替换缺失值
    data.replace(to_replace='?', value=np.nan)
    #
    data = data.dropna()

    x_train, x_test, y_train, y_test = train_test_split(data[column[1:10]], data[column[10]], test_size=0.25)

    ss_train = StandardScaler()
    x_train = ss_train.fit_transform(x_train)
    x_test = ss_train.transform(x_test)

    lgr = LogisticRegression(penalty='l2', C=1.2)

    lgr.fit(x_train, y_train)

    y_predicted = lgr.predict(x_test)
    print(lgr.coef_)
    print(lgr.score(x_train, y_test))
    print(classification_report(y_test, y_predicted, labels=[2, 4], target_names=['良性', '恶性']))
    return None


if __name__ == '__name__':
    logi()
