#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import jieba
import json
import jieba.posseg as psg
import numpy as np

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

with open("./test.json", 'r', encoding='utf-8') as file:
    for line in file.readlines():
        dic = json.loads(line)
        # print(dic['points'][2], list(i.word for i in psg.cut(dic['stem']) if i.flag in expectedNature))
        workslist.append(" ".join(list(i.word for i in psg.cut(dic['stem']) if i.flag in expectedNature)))
        titlelist.append(dic['pointsName'])
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
weight = tfidf.toarray()

print('ssss')
n = 10

for (title, w) in zip(titlelist, weight):
    print(u'{}:'.format(title))
    # 排序
    loc = np.argsort(-w)
    for i in range(n):
        print(u'-{}: {} {}'.format(str(i + 1), words[loc[i]], w[loc[i]]))
    print('\n')

    # for i in range(len(weight)):
    #     print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
    #     for j in range(len(word)):
    #         print(word[j], weight[i][j])
