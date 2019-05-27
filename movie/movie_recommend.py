#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import math

__author__ = 'the king of north'

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


# 余弦
def calCosineSimilrity(list1, list2):
    res = 0
    deniminator1 = 0
    deniminator2 = 0
    for (val1, val2) in zip(list1, list2):
        res += (val1 * val2)
        deniminator1 += val1 ** 2
        deniminator2 += val2 ** 2
    return res / (math.sqrt(deniminator1 * deniminator2))


moviesPath = '../ml-1m/movies.csv'
ratingsPath = '../ml-1m/ratings.csv'

moviesDF = pd.read_csv(moviesPath)
ratingsDF = pd.read_csv(ratingsPath)

# print(len(moviesDF["MovieID"].values.tolist()))

trainRatingsDF, testRatingsDF = train_test_split(ratingsDF, test_size=0.2)

# 透视
# 获得一张用户-电影的评分矩阵
trainRatingsPivotDF = pd.pivot_table(trainRatingsDF[['UserID', 'MovieID', 'Rating']], columns=['MovieID'],
                                     index=['UserID'], values='Rating')
# 电影id和用户id与其对应索引的映射关系
moviesMap = dict(enumerate(list(trainRatingsPivotDF.columns)))
usersMap = dict(enumerate(list(trainRatingsPivotDF.index)))
ratingsValues = trainRatingsPivotDF.values.tolist()

# print(ratingsValues)
# print(len(ratingsValues))

# 用户相似度计算
userSimMatrix = np.zeros((len(ratingsValues), len(ratingsValues)), dtype=np.float32)
# print(userSimMatrix)
print(len(ratingsValues) * len(ratingsValues))
for i in range(len(ratingsValues) - 1):
    for j in range(len(ratingsValues) - 1):
        userSimMatrix[i, j] = calCosineSimilrity(ratingsValues[i], ratingsValues[j])
        userSimMatrix[j, i] = userSimMatrix[i, j]
        # print(1)
print(userSimMatrix)
