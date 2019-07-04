#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'
# https://blog.csdn.net/qq5q13638/article/details/78379817
import numpy as np
from sklearn import metrics

y = np.array([1, 1, 2, 2])
pred = np.array([0.1, 0.4, 0.35, 0.8])
fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=2)
metrics.auc(fpr, tpr)
