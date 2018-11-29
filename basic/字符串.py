#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'

import string

var1 = 'Hello World!'
var2 = "Python Runoob"
var3 ='abc'


print("var1[0]: ", var1[0])
print("var2[1:5]: ", var2[1:5])


print(var1[:6])
print ("更新字符串 :- ", var1[:6] + 'Runoob!')

print(string.capwords(var3))