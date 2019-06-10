#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import tensorflow as tf

# 张量
a = tf.constant([1, 2, 3, 4, 5])

# 1，变量能够持久化保存，普通的张量op是不行的
# 2，当定义一个变量op的时候，一定在会话当中去初始化
var = tf.Variable(tf.random_normal([2, 3], mean=0.0, stddev=1.0))

print(a, var)
# 必须做一步显示的初始化
init_op = tf.global_variables_initializer()

with tf.Session() as sess:
    # 必须运行初始化op
    sess.run(init_op)

    print(sess.run([a, var]))
    # 可视化
    # tensorboard --logdir="23深度学习/04-变量和模型保存加载/show/"
    filewriter = tf.summary.FileWriter("show", graph=sess.graph)




