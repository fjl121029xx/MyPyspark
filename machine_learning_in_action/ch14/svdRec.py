#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy
import tensorflow as tf
from numpy import *
from numpy import linalg as la


def load_ex_data():
    return [
        [1, 1, 1, 0, 0],
        [2, 2, 2, 0, 0],
        [5, 5, 5, 0, 0],
        [1, 1, 0, 2, 2],
        [0, 0, 0, 3, 3],
        [0, 0, 0, 1, 1],
    ]


def load_ex_data2():
    return [
        [4, 4, 0, 2, 2],
        [4, 0, 0, 3, 3],
        [4, 0, 0, 1, 1],
        [1, 1, 1, 2, 0],
        [2, 2, 2, 0, 0],
        [1, 1, 1, 0, 0],
        [5, 5, 5, 0, 0]

    ]


def load_ex_data_big():
    return [
        [2, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0],
        [3, 3, 4, 0, 3, 0, 0, 2, 2, 0, 0],
        [5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0],
        [4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0],
        [0, 0, 0, 3, 0, 0, 0, 0, 4, 5, 0],
        [1, 1, 2, 1, 1, 2, 1, 0, 4, 5, 0]

    ]


def euclid_sim(in_a, in_b):
    return 1.0 / (1.0 + la.norm(in_a - in_b))


def pears_sim(in_a, in_b):
    if len(in_a) < 3:
        return 1.0
    return 0.5 + 0.5 * corrcoef(in_a, in_b, rowvar=0)[0][1]


def cos_sim(in_a, in_b):
    # print('in_a', in_a, 'in_b', in_b)
    num = float(in_a.T * in_b)
    denom = la.norm(in_a) * la.norm(in_b)
    if denom == 0:
        return 0.0
    return 0.5 + 0.5 * (num / denom)


# 推荐系统的工作过程是：给定一个用户，系统会为此用户返回N个最好的推荐菜。
# 1.
# 2.
# 3.

# 计算在给定相似度计算方法的条件下，用户对物品的估计评分值
# 数据矩阵、用户编号、物品编号和相似度计算方法
def stand_est(data_mat, user, sim_meas, item):
    n = shape(data_mat)[1]
    sim_total = 0.0
    rat_sim_total = 0.0
    for j in range(n):
        user_rating = data_mat[user, j]
        if user_rating == 0:
            continue
        # 两个物品当中已经被评分的那个元素
        over_lap = nonzero(logical_and(data_mat[:, item].A > 0,
                                       data_mat[:, j].A > 0))
        # print('item', item, 'j', j, 'over_lap', over_lap)
        # print('over_lap[0]', over_lap[0])
        # print(type(over_lap[0]))
        # 如果两种没有任何重合元素
        if len(over_lap) == 0:
            similarity = 0
        else:
            similarity = sim_meas(data_mat[over_lap[0], item],
                                  data_mat[over_lap[0], j])
        sim_total += similarity
        rat_sim_total += similarity * user_rating
        if sim_total == 0:
            return 0
    else:
        return rat_sim_total / sim_total


# 推荐引擎
def recommend(data_mat, user, n=3, sim_meas=cos_sim, est_method=stand_est):
    unrated_items = nonzero(data_mat[user, :].A == 0)[1]
    # print(unratedItems)
    if len(unrated_items) == 0:
        return 'you rated everything'
    itemScores = []
    for item in unrated_items:
        estimatedScore = est_method(data_mat, user, sim_meas, item)
        itemScores.append((item, estimatedScore))
    return sorted(itemScores, key=lambda jj: jj[1], reverse=True)[:n]


# item 1 j 0 over_lap (array([0, 3, 4, 5, 6], dtype=int64), array([0, 0, 0, 0, 0], dtype=int64))
print(nonzero(logical_and([4, 4, 4, 1, 2, 1, 5],
                          [4, 0, 0, 1, 2, 1, 5])))


# 基于svd的评分估计
def svd_est(data_mat, user, sim_meas, item):
    n = shape(data_mat)[1]
    sim_total = 0.0
    rat_sim_total = 0.0
    U, Sigma, VT = la.svd(data_mat)
    Sig4 = mat(eye(4) * Sigma[:4])
    xformed_items = data_mat.T * U[:, :4] * Sig4.I
    for j in range(n):
        user_rating = data_mat[user, j]
        if user_rating == 0 or j == item:
            continue
        similarity = sim_meas(xformed_items[item, :].T, xformed_items[j:].T)
        print('the %d and %d similarity is :%f' % (item, j, similarity))
        sim_total += similarity
        rat_sim_total += similarity * user_rating
    if sim_total == 0:
        return 0
    else:
        return rat_sim_total / sim_total
