#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

from sklearn.datasets import load_iris
from sklearn.decomposition import PCA, LatentDirichletAllocation

iris = load_iris()
print(LatentDirichletAllocation(n_components=2).fit_transform(iris.data, iris.target))
