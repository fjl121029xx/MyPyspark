#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

"""
    knn 用户签到位置
    特征值：x，y坐标，定位准确性，年，日，时，周   
    目标值：入住位置的Id
    
    https://storage.googleapis.com/kaggle-competitions-data/kaggle/5186/train.csv.zip?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1552497034&Signature=fCb13p%2BZCQQqnDk%2FPpDNgsxzB1efHitdOkmwjlbi0jCNV18qj457OIMAjGtuYKxgj7f4fbaUKC8DT%2Bmdg%2BatfudC6ORUG4D6Ia2hAA12wAyhfAvLXZRQt8vAcDxjagFEUR%2Fr%2F5BEnkCevnn5llkjgbw%2BYGto5LKOvF0DjcU%2BZX%2FLfN3hj1jkaGGsa75WOj0aER2oxixU8QA5SqqwvfZ%2BQC690VmwKr%2BRSxKla0fFvxy%2F9SWuar1Mx7JJYHJfKLsmrRsfEG3SVJNUJLSucd5NoKJZRfS5U4vILu7QSyYGGYxNOp1rnxBszE4P3W8NMjwKseddaIBceeMJRXgZT4U1KA%3D%3D
"""


def knncls():
    # 读取数据
    data = pd.read_csv('D:/work/train.csv/train.csv')
    # print(data.head(10))

    # 处理数据
    # 1、缩小数据范围
    data = data.query("x > 1.0 & x < 1.25 & y > 2.5 & y < 2.75")
    # 处理时间
    time_value = pd.to_datetime(data['time'], unit='s')
    # print(time_val)
    # 把日期格式转成字典数据
    time_value = pd.DatetimeIndex[time_value]
    # 构造一些特征
    data['day'] = time_value.day
    data['hour'] = time_value.hour
    data['weekday'] = time_value.weekday
    # 删除时间戳
    data = data.drop(['time'], axis=1)
    print(data)
    # 把签到数量少于n个目标位置删除
    place_count = data.groupby('place_id').count()
    tf = place_count[place_count.row_id > 3].reset_index()

    data = data[data['place_id'].isin(tf.place_id)]
    # 取出数据当中的特征值和目标值
    y = data['place_id']
    x = data.drop(['place_id'], axis=1)
    # 数据分割
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # 特征工程(标准化)
    std = StandardScaler()
    std_x_train = std.transform(x_train)
    std_y_train = std.transform(y_train)
    # 算法
    knn = KNeighborsClassifier(n_neighbors=5)
    # knn.fit(x_train, y_train)
    # 标准化之后
    knn.fit(std_x_train, std_y_train)

    # 得出预测结果
    y_predict = knn.predict(x_test)
    print("预测的目标签到位置：", y_predict)
    # 得出准确率
    print("预测准确率，", knn.score(x_test, y_test))

    return None


if __name__ == '__main__':
    knncls()
