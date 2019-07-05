#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split, cross_val_score

# 垃圾回收
column = ['label', 'message']
df = pd.read_csv('SMSSpamCollection.txt', delimiter='\t', header=None, names=column)
df['label'] = pd.factorize(df['label'])[0]
print(df.head())

# 用pandas加载数据.csv文件，然后用train_test_split分成训练集（75%）和测试集（25%）：
X_train_raw, X_test_raw, y_train, y_test = train_test_split(df['message'], df['label'], test_size=0.25)
# 我们建一个TfidfVectorizer实例来计算TF-IDF权重：
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train_raw)
X_test = vectorizer.transform(X_test_raw)
# LogisticRegression同样实现了fit()和predict()方法
classifier = LogisticRegression()
classifier.fit(X_train, y_train)
predictions = classifier.predict(X_test)
predictions_proba = classifier.predict_proba(X_test)
print(predictions_proba)

for i, prediction in enumerate(predictions[-5:]):
    print('预测类型：%s.信息：%s.' % (prediction, X_test_raw.iloc[i]))

print(classification_report(y_test, predictions, labels=['0', '1'], target_names=['ham', 'spam']))
print(classifier.score(X_test, y_test))

scores = cross_val_score(classifier, X_train, y_train, cv=5)
print('准确率', np.mean(scores), scores)

precisions = cross_val_score(classifier, X_train, y_train, cv=5, scoring='precision')
print(u'精确率：', np.mean(precisions), precisions)
recalls = cross_val_score(classifier, X_train, y_train, cv=5, scoring='recall')
print(u'召回率：', np.mean(recalls), recalls)
fls = cross_val_score(classifier, X_train, y_train, cv=5, scoring='f1')
print('综合指标评价', np.mean(fls), fls)
plt.scatter(recalls, precisions)
plt.show()
