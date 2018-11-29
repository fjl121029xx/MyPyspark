#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'

dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}

print("dict['Name']: ", dict['Name'])
print("dict['Age']: ", dict['Age'])

dict['Age'] = 8  # 更新
dict['School'] = "RUNOOB"  # 添加

print("dict['Age']: ", dict['Age'])
print("dict['School']: ", dict['School'])