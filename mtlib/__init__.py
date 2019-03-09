#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

from matplotlib import pyplot as plt
import numpy as np

# 大小 清晰度
fig = plt.figure(figsize=(20, 8), dpi=80)

x = np.array([2, 4, 8, 10, 12, 14, 16, 18, 20, 22, 24])
y = np.array([15, 13, 14, 17, 20, 25, 26, 24, 22, 18, 15])

# x = np.array([0.46,0.59,0.68,0.99,0.39,0.31,1.09,
#               0.77,0.72,0.49,0.55,0.62,0.58,0.88,0.78])
# y = np.array([0.315,0.383,0.452,0.650,0.279,0.215,0.727,0.512,
#               0.478,0.335,0.365,0.424,0.390,0.585,0.511])


# 设置x轴刻度
_xtick_labels = [i / 2 for i in range(2, 49)]
plt.xticks(_xtick_labels)
plt.yticks(range(min(y), max(y) + 1, 1))

plt.plot(x, y)
# plt.savefig("./sig_size.png")
plt.show()
