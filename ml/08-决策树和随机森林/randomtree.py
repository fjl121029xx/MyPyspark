#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

"""
    随机深林预测Titanic生存者
    D:/work/Titanic/gender_submission.csv
    D:/work/Titanic/test.csv
    D:/work/Titanic/train.csv
"""


def rt():
    """

    :return:
    """
    titanic = pd.read_csv("D:/work/Titanic/train.csv")

    # 处理数据,找出特征值和目标是
    x = titanic[['Pclass', 'Age', 'Sex']]
    y = titanic['Survived']

    # 处理缺失值
    x['Age'].fillna(x['Age'].mean(), inplace=True)

    # 分割训练集和测试集

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    dict = DictVectorizer(sparse=False)
    x_train = dict.fit_transform(x_train.to_dict(orient='records'))
    print(dict.get_feature_names())

    x_test = dict.transform(x_test.to_dict(orient='records'))

    rmt = RandomForestClassifier()
    param = {"n_estimators": [120, 200, 300, 500, 800, 1200], "max_depth": [5, 15, 25, 30]}
    gc = GridSearchCV(rmt, param_grid=param, cv=2)

    gc.fit(x_train, y_train)
    print("gc在测试集上的准确率：", gc.score(x_test, y_test))
    print("gc选择最好的模型是：", gc.best_params_)
    return None


if __name__ == '__main__':
    rt()
