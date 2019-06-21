#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy
import tensorflow as tf

a = tf.constant([1.0, 2.0], name="a")
b = tf.constant([[2.0, 3.0], [2.0, 3.0]], name="b")

result = a * b

zerp = tf.zeros(shape=[10, 10], dtype=tf.float32, name="a")

# 创建随机张量
rn = tf.random_normal(shape=[10, 10], mean=0.0, stddev=1.0, dtype=tf.float32, seed=10, name="rn")

with tf.Session() as sess:
    # print(sess.run(result))
    # print(zerp)
    # print(sess.run(zerp))
    print(sess.run(rn))
