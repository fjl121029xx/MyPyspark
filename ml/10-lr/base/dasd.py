#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from mlxtend.evaluate import plot_decision_regions

column = ['Sample code number', 'Clump Thickness ', 'Uniformity of Cell Size', 'Uniformity of Cell Shape',
          'Marginal Adhesion', 'Single Epithelial Cell Size ', 'Bare Nuclei ',
          'Bland Chromatin', 'Normal Nucleoli', 'Mitoses', 'Class']
data = pd.read_csv(
    '../breast-cancer-wisconsin.data',
    names=column)

data.replace(to_replace='?', value=np.nan, inplace=True)
data = data.dropna()

x_train, x_test, y_train, x_test = train_test_split(data[column[1:10]], data[column[10]], test_size=0.25)
ss_train = StandardScaler()
x_train = ss_train.fit_transform(x_train)
x_test = ss_train.transform(x_test)

lr = LogisticRegression(C=100.0, random_state=1)
lr.fit(x_train, y_train)

plot_decision_regions(X=x_test,
                      y=x_test,
                      classifier=lr,
                      test_idx=range(105, 150))
plt.xlabel('petal length [standardized]')
plt.ylabel('petal width [standardized]')
plt.legend(loc='upper left')
plt.tight_layout()
# plt.savefig('images/03_06.png', dpi=300)
plt.show()
