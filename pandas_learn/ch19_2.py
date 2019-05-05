#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
# 19 连接数据库
# https://www.jb51.net/article/138551.htm
import numpy as np
import pandas as pd
import pymysql

conn = pymysql.connect(host='192.168.100.18', port=3306, user='vhuatu', passwd='vhuatu_2013', db='vhuatu',
                       charset='utf8')

sql = 'select * from v_qbank_user limit 0,10'

df = pd.read_sql(sql, con=conn, index_col=['uname', 'last_login_time'])
print(df.head())
conn.close()

# 3 index_col规定将哪一列数据设置为index
