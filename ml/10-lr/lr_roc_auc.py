#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, accuracy_score, roc_curve
import matplotlib.pyplot as plt


class LRROCAIC:

    def __init__(self, path, columns):
        data_all = pd.read_csv(path, names=columns)
        # 替换缺失值
        data_all.replace(to_replace='?', value=np.nan, inplace=True)
        data_all = data_all.dropna()
        self.X = data_all[column[1:10]]
        self.Y = data_all[column[10]]

    def create_fit_data(self):
        ss_train = StandardScaler()
        x_train, x_test, y_train, y_test = train_test_split(self.X, self.Y, test_size=0.3)
        x_train_stand = ss_train.fit_transform(x_train)
        x_test_stand = ss_train.fit_transform(x_test)
        return x_train_stand, x_test_stand, y_train, y_test


if __name__ == '__main__':
    column = ['Sample code number', 'Clump Thickness ', 'Uniformity of Cell Size', 'Uniformity of Cell Shape',
              'Marginal Adhesion', 'Single Epithelial Cell Size ', 'Bare Nuclei ',
              'Bland Chromatin', 'Normal Nucleoli', 'Mitoses', 'Class']

    lr = LRROCAIC('breast-cancer-wisconsin.data', column)
    x_train_stand, x_test_stand, y_train, y_test = lr.create_fit_data()
    lr = LogisticRegression(penalty='l2', C=1.2)  # 逻辑回归模型
    lr.fit(x_train_stand, y_train)
    lr_y_proba = lr.predict_proba(x_test_stand)
    lr_y_pre = lr.predict(x_test_stand)

    lr_score = lr.score(x_test_stand, y_test)
    lr_accuracy_score = accuracy_score(y_test, lr_y_pre)
    lr_preci_score = precision_score(y_test, lr_y_pre)
    lr_recall_score = recall_score(y_test, lr_y_pre)
    lr_f1_score = f1_score(y_test, lr_y_pre)
    lr_auc = roc_auc_score(y_test, lr_y_proba[:, 1])
    print('lr_accuracy_score: %f,lr_preci_score: %f,lr_recall_score: %f,lr_f1_score: %f,lr_auc: %f'
          % (lr_accuracy_score, lr_preci_score, lr_recall_score, lr_f1_score, lr_auc))
