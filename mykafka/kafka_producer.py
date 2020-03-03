#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import json
from kafka import KafkaProducer
import time

# https://blog.csdn.net/see_you_see_me/article/details/78468421
# https://blog.csdn.net/luanpeng825485697/article/details/81036028

producer = KafkaProducer(bootstrap_servers='192.168.65.132:9092')

a = 1
while a < 1000000:
    msg_dict = {"id": a, "name": "tom" + str(a), "score": 3.14 * a}
    msg = json.dumps(msg_dict)
    producer.send('bd_canal_order_tbl_order_master', msg.encode(), partition=0)
    a += 1
    time.sleep(2)

producer.close()
