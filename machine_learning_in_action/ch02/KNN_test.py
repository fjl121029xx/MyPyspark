#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import KNN
import pandas as pd
import numpy as np
import tensorflow as tf
import operator
from numpy import *
import operator
from os import listdir

group, label = KNN.createDataSet()
target = KNN.classify0(inX=[0.1, 0.1], dataSet=group, labels=label, k=3)

arr = array([[1.2, 2.5], [2.3, 5.0]])
print("arr", arr.shape[0])
matArr = arr
print(matArr)
print(type(matArr))
print(matArr ** 2)


