#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'

str = input("请输入：")
print("你输入的内容是: ", str)


# 打开一个文件
fo = open("support.py", "w")
print ("文件名: ", fo.name)
print ("是否已关闭 : ", fo.closed)
print ("访问模式 : ", fo.mode)
print ("末尾是否强制加空格 : ", fo.softspace)