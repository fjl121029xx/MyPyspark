#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'
"""
https://yq.aliyun.com/articles/335620
"""
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns

diabetes = pd.read_csv('./diabetes.csv')

print(diabetes.columns)
print(diabetes.head())
print("dimension of diabetes data: {}".format(diabetes.shape))
print(diabetes.groupby('Outcome').size())

sns.countplot(diabetes['Outcome'], label="Count")
print(diabetes.info())
