#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

from sklearn.feature_extraction import DictVectorizer


def dictvec():
    """

    :return:
    """
    # 实例化
    dict = DictVectorizer(sparse=False)

    data = dict.fit_transform([{'city': '北京', 'temperature': 100},
                               {'city': '上海', 'temperature': 60},
                               {'city': '北京', 'temperature': 90},
                               {'city': '武汉', 'temperature': 30}])

    print(dict.get_feature_names())
    print(data)
    return None


if __name__ == "__main__":
    dictvec()
