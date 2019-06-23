#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy as np
from numpy import *

# print(random.rand(4, 4))
randMat = mat(random.rand(4, 4))

# 逆矩阵
myEye = invRandMat = randMat.I
print(myEye - eye(4))
