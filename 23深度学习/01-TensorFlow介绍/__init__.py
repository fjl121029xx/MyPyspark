#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

import tensorflow as tf

# 创建一张图，上下文环境
g = tf.Graph()
with g.as_default():
    c = tf.constant(11.0)
    print(c.graph)

# 加法
a = tf.constant(5.0)
b = tf.constant(6.0)

print(a, b)

sum1 = tf.add(a, b)

gra = tf.get_default_graph()
print(gra)
print(sum1)

plt = tf.placeholder(tf.float32, [None, 3])
print(plt)
with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
    print(sess.run(plt, feed_dict={plt: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}))
    # print(sess.run(sum1))

# with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
#     print(sess.run(sum1))
