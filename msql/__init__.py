#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

"""
 Python MySQL - mysql-connector 驱动
https://www.runoob.com/python3/python3-mysql.html
"""

import pymysql

# 打开数据库连接
db = pymysql.connect("192.168.100.154", "vhuatu", "vhuatu_2013", "vhuatu")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()

print("Database version : %s " % data)

# 关闭数据库连接
db.close()
