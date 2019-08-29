#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

# 超级详细的协同过滤推荐系统+完整Python实现及结果
# https://blog.csdn.net/qq_25948717/article/details/81839463

"""
但有时我们会碰到因为两个用户之间数据由于数据膨胀，一方数据大，一方数据小，但是两者称明显的线性关系

我们引入Pearson相关系数来衡量两个变量之间的线性相关性。

Pearson：-1~1   -1：完全负相关  1：完全正相关  0：不相关              

相关系数 0.8-1.0 极强相关

0.6-0.8 强相关

0.4-0.6 中等程度相关

0.2-0.4 弱相关

0.0-0.2 极弱相关或无相关
"""
from math import *

file = open("../../ml-1m/data.csv", 'r',
            encoding='UTF-8')  # 记得读取文件时加‘r’， encoding='UTF-8'
# 读取data.csv中每行中除了名字的数据
# 存放每位用户评论的电影和评分
data = {}

for line in file.readlines():
    # 注意这里不是readline()
    line = line.strip().split(',')
    # 如果字典中没有某位用户，则使用用户ID来创建这位用户
    if not line[0] in data.keys():
        data[line[0]] = {line[3]: line[1]}
    # 否则直接添加以该用户ID为key字典中
    else:
        data[line[0]][line[3]] = line[1]


#########################################################################
# 计算两用户之间的Pearson相关系数
def pearson_sim(user1, user2):
    # 取出两位用户评论过的电影和评分
    user1_data = data[user1]
    user2_data = data[user2]
    distance = 0
    common = {}

    # 找到两位用户都评论过的电影
    for key in user1_data.keys():
        if key in user2_data.keys():
            common[key] = 1
    if len(common) == 0:
        return 0  # 如果没有共同评论过的电影，则返回0
    n = len(common)  # 共同电影数目
    print(n, common)

    # 计算评分和
    sum1 = sum([float(user1_data[movie]) for movie in common])
    sum2 = sum([float(user2_data[movie]) for movie in common])

    # 计算评分平方和
    sum1Sq = sum([pow(float(user1_data[movie]), 2) for movie in common])
    sum2Sq = sum([pow(float(user2_data[movie]), 2) for movie in common])

    # 计算乘积和
    PSum = sum([float(user1_data[it]) * float(user2_data[it]) for it in common])

    # 计算相关系数
    num = PSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    r = num / den
    return r


R = pearson_sim('1', '3')
print(R)
