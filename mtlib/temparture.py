#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

from matplotlib import pyplot as plt
import random
import matplotlib
import numpy as np
from matplotlib import font_manager

font = {'family': 'sans-serif',
        'size': '15'}

matplotlib.rc('font', **font)

x = range(0, 120)
y = [random.randint(20, 35) for i in range(120)]

plt.figure(figsize=(20, 8), dpi=100)

_x = list(x)[::3]
_xticks_labels = ["10:{}".format(i) for i in range(60)]
_xticks_labels += ["11:{}".format(i - 60) for i in range(60, 120)]
plt.xticks(_x, _xticks_labels[::3], rotation=30)

# 添加描述信息
plt.xlabel('time')
plt.ylabel('temperture')
plt.title('temperture record')

plt.grid()

plt.plot(x, y)
plt.savefig("./sig_size.png")
plt.show()
