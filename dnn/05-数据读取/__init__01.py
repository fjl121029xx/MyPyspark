#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import tensorflow as tf

# 1\首先定义队列

Q = tf.FIFOQueue(3, tf.float32)

en_qmany = Q.enqueue_many([[0.1, 0.2, 0.3], ])

# 2\d

out_q = Q.dequeue()

data = out_q + 1

en_q = Q.enqueue(data)

with tf.Session() as sess:
    sess.run(en_qmany)

    # 处理数据
    for i in range(100):
        sess.run(en_q)

    for i in range(Q.size().eval()):
        print(sess.run(Q.dequeue()))
