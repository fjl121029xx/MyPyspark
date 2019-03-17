#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import tensorflow as tf

# 1\首先定义队列
Q = tf.FIFOQueue(1000, tf.float32)

# 2\定义要做的事情
var = tf.Variable(0.0, tf.float43 == 32)

# 自增
data = tf.assign_add(var, tf.constant(1.0))

en_q = Q.enqueue(data)

# 3\定义队列管理器op
qr = tf.train.QueueRunner(Q, enqueue_ops=[en_q]*2)

# 2\d
init_op = tf.global_variables_initializer()


with tf.Session() as sess:
    #
    sess.run(init_op)

    # 线程管理器
    coord= tf.train.Coordinator()

    # 开启线程
    t1 =qr.create_threads(sess,coord=coord,start=True)

    # 主线程
    for i in range(Q.size().eval()):
        print(sess.run(Q.dequeue()))

    #
    coord.request_stop()
    coord.join(t1)
