#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

"""
使用python来操作redis用法详解
https://www.jianshu.com/p/2639549bedc8
"""
import redis

r = redis.Redis(host='192.168.100.20', port=6379,
                decode_responses=True)  # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
r.set('name', 'junxi')  # key是"foo" value是"bar" 将键值对存入redis缓存
print(r['name'])
print(r.get('name'))  # 取出键name对应的值
print(type(r.get('name')))
