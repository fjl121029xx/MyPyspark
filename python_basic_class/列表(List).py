#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'

list1 = ['physics', 'chemistry', 1997, 2000]
list2 = [1, 2, 3, 4, 5, 6, 7]

print("list1[0]: ", list1[0])
print("list2[1:5]: ", list2[1:5])

list = []  ## 空列表
list.append('Google')  ## 使用 append() 添加元素
list.append('Runoob')
print(list)

list1 = ['physics', 'chemistry', 1997, 2000]

print(list1)
del list1[2]
print("After deleting value at index 2 : ")
print(list1)
