#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

from sklearn.naive_bayes import MultinomialNB
from sklearn.datasets import load_iris, fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report


"""
    朴素贝叶斯 文本分类
   D:/work/20_newsgroups 
"""


def nb():
    """

    :return:
    """
    news = fetch_20newsgroups(subset='all')
    # 进行数据分割
    x_train, x_test, y_train, y_test = train_test_split(news.data, news.target, test_size=0.25)

    # 对数据集进行特征抽取
    tf = TfidfVectorizer()

    # 以训练集当中的词的列表进行每篇文章重要性统计
    x_train = tf.fit_transform(x_train)
    print(tf.get_feature_names())
    x_test = tf.transform(x_test)

    # 朴素贝叶斯算法
    mlt = MultinomialNB(alpha=1.0)
    print(x_train)
    mlt.fit(x_train, y_train)

    y_predict = mlt.predict(x_test)
    print(y_predict)
    print(mlt.score(x_test, y_test))

    # 召回率
    print(classification_report(y_test, y_predict, target_names=news.target_names))
    return None


if __name__ == '__main__':
    nb()
