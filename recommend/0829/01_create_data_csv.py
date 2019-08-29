#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

# 超级详细的协同过滤推荐系统+完整Python实现及结果
# https://blog.csdn.net/qq_25948717/article/details/81839463

"""
@Company：华中科技大学电气学院聚变与等离子研究所
@version: V1.0
@author: YEXIN
@contact: 1650996069@qq.com or yexin@hust.edu.cn 2018--2020
@software: PyCharm
@file: recommend.py
@time: 2018/8/19 17:32
@Desc：读取用户的电影数据和评分数据
"""
import pandas as pd

import os

print(os.path.abspath(__file__))
movies = pd.read_csv("../../ml-1m/movies.csv")
ratings = pd.read_csv("../../ml-1m/ratings.csv")  ##这里注意如果路径的中文件名开头是r，要转义。
data = pd.merge(movies, ratings, on='movieId')  # 通过两数据框之间的movieId连接
data[['userId', 'rating', 'movieId', 'title']].sort_values('userId').to_csv(
    '../../ml-1m/data.csv', index=False)
