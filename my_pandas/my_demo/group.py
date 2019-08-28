#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

data = pd.read_csv('../si.csv', names=['name', 'terminal', 'b', 'c'])
data = data.replace(to_replace=np.nan, value=0)

print(data.groupby('terminal').sum())
