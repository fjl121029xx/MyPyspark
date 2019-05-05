#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 19 连接数据库
# https://blog.csdn.net/heshiliqiu/article/details/81590685
import numpy as np
import pandas as pd
import pymysql

db = pymysql.connect(host='192.168.100.18', port=3306, user='vhuatu', passwd='vhuatu_2013', db='vhuatu', charset='utf8')
cursor = db.cursor()

sql = 'select * from v_qbank_user limit 0,10'

cursor.execute(sql)
info = cursor.fetchall()

db.commit()
cursor.close()
db.close()

print(info)
print(info[0][0])

print(pd.DataFrame(info))
