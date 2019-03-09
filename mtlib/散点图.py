#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

from matplotlib import pyplot as plt
import numpy as np

N = 1000
x = np.random.randn(N)
y = np.random.randn(N)
plt.scatter(x, y)
plt.show()

