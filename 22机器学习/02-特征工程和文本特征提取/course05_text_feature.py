#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

import jieba
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def textvec():
    """

    :return:
    """
    vector = CountVectorizer()
    # res = vector.fit_transform(["人生苦短,我喜欢python ", "人生漫长，不要python了"])
    res = vector.fit_transform(["lift is short,i like python", "life is to long,i dislike python"])

    print(vector.get_feature_names())

    print(res.toarray())


def cutword():
    """

    :return:
    """
    con1 = jieba.cut("今天很残酷，明天更残酷，后天很美好，但绝对不部分是死在明天晚上，所以每个人不要放弃今天。")
    con2 = jieba.cut("我们看到的从很远星系来的光是在几百万年之前发出的，这样当我们看到宇宙时，我们是在看它的过去。")
    con3 = jieba.cut("如果只用一种方式了解某样事务，你就不会真正了解它。了解事务真正含义的秘密取决于如何将其他与我们所了解的事务相联系")

    # 转换成列表
    content1 = list(con1)
    content2 = list(con2)
    content3 = list(con3)

    #
    c1 = ' '.join(content1)
    c2 = ' '.join(content2)
    c3 = ' '.join(content3)

    return c1, c2, c3


def hanzivec():
    """
    中文特征值化
    :return:
    """
    vector = TfidfVectorizer()
    # vector = CountVectorizer()

    c1, c2, c3 = cutword()
    res = vector.fit_transform([c1, c2, c3])

    print(vector.get_feature_names())

    print(res.toarray())
    return None


if __name__ == '__main__':
    hanzivec()
