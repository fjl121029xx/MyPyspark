#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'

for letter in 'Python':  # 第一个实例
    if letter == 'h':
        continue
    print('当前字母 :', letter)

var = 10  # 第二个实例
while var > 0:
    var = var - 1
    if var == 5:
        continue
    print('当前变量值 :', var)
print("Good bye!")
