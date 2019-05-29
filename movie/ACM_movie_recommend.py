#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'

import numpy as np
import pandas as pd

# 1.输入电影的标题和用户图谱
# 2.采用content-based模型计算25个最相似的电影
# 3.使用协同滤波模型对该用户的25个电影计算评分
# 4.参考最高的预测分数返回最高的前10个电影

#
cosine_sim = pd.read_csv('../data/cosine_sim.csv')
consine_sim_map = pd.read_csv('../data/cosine_sim_map.csv', header=None)

consine_sim_map = consine_sim_map.set_index(0)
consine_sim_map = consine_sim_map[1]

from surprise import SVD, Reader, Dataset

reader = Reader()
ratings = pd.read_csv('D:\idea\the-movies-dataset')
