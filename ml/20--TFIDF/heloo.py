#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import jieba
import json
import jieba.posseg as psg
import numpy as np
import pandas as pd
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

# 由于文件中有多行，直接读取会出现错误，因此一行一行读取
workslist = []
titlelist = []
# 保留词性
expectedNature = [
    "n", "v", "vd", "vn", "vf",
    "vx", "vi", "vl", "vg", "nt",
    "nz", "nw", "nl", "ng", "userDefine", "wh"]

chunkSize = 1000
chunks = []

# with open("./test.json", 'r',
#           encoding='utf-8') as file:
with open("E:\\ztk_question_new\\part-00000-52499296-627b-4c67-b8e5-06a93507a3d3-c000.json", 'r',
          encoding='utf-8') as file:
    file.readline()
    for line in file.readlines():
        dic = json.loads(line)
        # print(dic['points'][2], list(i.word for i in psg.cut(dic['stem']) if i.flag in expectedNature))
        # print(line)
        keys = dic.keys()
        if 'stem' in keys:
            titlelist.append(dic['_id'])
            workslist.append(" ".join(list(i.word for i in psg.cut(dic['stem']) if i.flag in expectedNature)))
        else:
            pass
# print(len(workslist))
# print(len(titlelist))
# print(titlelist)
# print(corpus)

vectorizer = CountVectorizer()

# 计算每个词语出现的次数
X = vectorizer.fit_transform(workslist)

# 获取词袋中所有文本关键词
words = vectorizer.get_feature_names()
# print(word)
# 查看词频结果
# print(X.toarray())

transformer = TfidfTransformer()

tfidf = transformer.fit_transform(X)
# print(type(tfidf))
# print(tfidf)
# weight = tfidf.toarray()


print('ssss')
n = 10

# print(workslist[0])
print(u'{}:'.format(titlelist[0]))

w = tfidf[0, :].data

loc = np.argsort(-w)
print("w", w[loc][0:10])

# for i in range(10):
#     print(u'{}:{}'.format(str(i + 1), loc[i]))

p = workslist[0].split(" ")
# print("p", p)

po = []
for i in p:
    try:
        if tfidf[0, words.index(i)] > 0:
            po.append(i)
    except ValueError:
        pass

# print(po)
print(np.array(po)[loc][0:10])

# print("f(p)", [loc])
#
# for (title, w) in zip(titlelist, weight):
#     print(u'{}:'.format(title))
#     # 排序
#     loc = np.argsort(-w)
#     for i in range(n):
#         print(u'-{}: {} {}'.format(str(i + 1), words[loc[i]], w[loc[i]]))
#     print('\n')
#
