#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 8 数据
import numpy as np
import pandas as pd

df = pd.DataFrame({
    'A': ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'bar'],
    'B': ['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
    'C': np.random.randn(8),
    'D': np.random.randn(8)
})

print(df)


# 3 对A列进行分组
# grouped = df.groupby('A')
# print(grouped.first())

# 4 两列以上分组
# grouped = df.groupby(['A', 'B'])
# print(grouped.last())


# 5 根据列分组
def get_type(letter):
    if letter.lower() in 'abem':
        print(letter)
        return 'vowel'
    else:
        return 'consonant'


grouped = df.groupby(get_type, axis=1)
print(grouped.first())
