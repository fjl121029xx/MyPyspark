#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

# 超级详细的协同过滤推荐系统+完整Python实现及结果
# https://blog.csdn.net/qq_25948717/article/details/81839463

"""
采用python字典来表示每位用户评论的电影和评分
"""
import pandas as pd

import os

print(os.path.abspath(__file__))

file = open("../../ml-1m/data.csv", 'r',
            encoding='UTF-8')  # 记得读取文件时加‘r’， encoding='UTF-8'
# 读取data.csv中每行中除了名字的数据
# 存放每位用户评论的电影和评分
data = {}

for line in file.readlines()[1:100]:
    # 注意这里不是readline()
    line = line.strip().split(',')
    # 如果字典中没有某位用户，则使用用户ID来创建这位用户
    if not line[0] in data.keys():
        data[line[0]] = {line[3]: line[1]}
    # 否则直接添加以该用户ID为key字典中
    else:
        data[line[0]][line[3]] = line[1]
print(data)
