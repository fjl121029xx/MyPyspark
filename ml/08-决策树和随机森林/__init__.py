#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

from sklearn.tree import DecisionTreeClassifier, export_graphviz
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
import graphviz
"""
    决策树预测Titanic生存者
    D:/work/Titanic/gender_submission.csv
    D:/work/Titanic/test.csv
    D:/work/Titanic/train.csv
"""


def tt():
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
    print(x_train)
    #
    dict = DictVectorizer(sparse=False)
    x_train = dict.fit_transform(x_train.to_dict(orient='records'))
    print(dict.get_feature_names())

    x_test = dict.transform(x_test.to_dict(orient='records'))

    print(x_train)
    dt = DecisionTreeClassifier()
    dt.fit(x_train, y_train)

    # 预测的准确率
    print("预测的准确率是：", dt.score(x_test, y_test))

    y_predict = dt.predict(x_test)
    print("预测值是：", y_predict)

    export_graphviz(dt, out_file="tree.dot", feature_names=['Age', 'Pclass', 'Sex=female', 'Sex=male'])
    return None


if __name__ == '__main__':
    tt()
