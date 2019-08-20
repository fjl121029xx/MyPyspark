#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

# 数据预处理

from sklearn.datasets import load_iris

# 无量纲化 ---> 标准化，区间缩放，归一化
from sklearn.preprocessing import StandardScaler, MinMaxScaler, Normalizer
# 对定量特征二值化 Binarizer(threshold=3).fit_transform(iris.data)
# 哑巴编码 OneHotEncoder().fit_transform(iris.target.reshape((-1, 1)))
from sklearn.preprocessing import Binarizer, OneHotEncoder

from numpy import vstack, array, nan
# 缺失值处理 Imputer().fit_transform(vstack((array([nan, nan, nan, nan]), iris.data)))
from sklearn.preprocessing import Imputer

# 基于多项式、指数函数、对数函数的数据变换ll
from sklearn.preprocessing import PolynomialFeatures

# 多项式转换 PolynomialFeatures().fit_transform(iris.data)

from numpy import log1p
from sklearn.preprocessing import FunctionTransformer

# 导入IRIS数据集
iris = load_iris()

print(FunctionTransformer(log1p).fit_transform(iris.data))
