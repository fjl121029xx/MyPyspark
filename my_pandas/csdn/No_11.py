#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy
import tensorflow as tf

arrays = [["bar", "bar", "baz", "baz", "foo", "foo"],
          ["one", "two", "one", "two", "one", "two"]]

tuples = list(zip(*arrays))
print(tuples)

index = pd.MultiIndex.from_tuples(tuples, names=['first', 'second'])
print(index)

s = pd.Series([3, 1, 4, 1, 5, 9], index=index)
print(s)
