#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy
import tensorflow as tf

# 以下产生了两个计算图，每个计算图中定义了一个名字为v的变量。

g1 = tf.Graph()
with g1.as_default():
    # 在计算图g1中定义变量v，并设置初始值为0
    v = tf.get_variable(
        "v", shape=[1], initializer=tf.zeros_initializer
    )

g2 = tf.Graph()
with g2.as_default():
    v = tf.get_variable(
        "v", shape=[1], initializer=tf.ones_initializer
    )

# 在计算图g1中读取变量v的取值
with tf.Session(graph=g1) as sess:
    tf.global_variables_initializer().run()
    with tf.variable_scope("", reuse=True):
        # 在计算图g1中，变量v的取值应该为0，所以下面这行会输出[0.]
        print(sess.run(tf.get_variable("v")))

with tf.Session(graph=g2) as sess:
    tf.global_variables_initializer().run()
    with tf.variable_scope("", reuse=True):
        print(sess.run(tf.get_variable("v")))
