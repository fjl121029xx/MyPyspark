#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'

a, b, c = 1, 2, "json"
print(a, b, c)

#######################
var1 = 1
var2 = 10
print(var1)
print(var2)
del var1
# print(var1)

###字符串###################
str = 'Hello World!'
s = 'abcded'
print(s[1:5])
print(s[1:])
print(str * 2)

###列表#####################
list = ['runoob', 76, 2.23, 'john', 70.2]
tinylist = [123, 'john']
print(list)
print(list[0])
print(list[1:3])
print(list[2:])
print(list + tinylist)

###元祖#####################
tuple = ('runoob', 786, 2.23, 'john', 70.2)
tinytuple = (123, 'john')
print(tuple + tinytuple)

###字典#####################
dict={}
dict['one']="this is one"
dict[2]="this is two"
tinydict={'name':'john','code':6374,'dept':'sales'}
print(dict['one'])
print(dict[2])
print(tinydict.keys())
print(tinydict.values())













