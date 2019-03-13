#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'

import tensorflow as tf

# # 构建图
# matrix1 = tf.constant([[3., 3.]])
#
# matrix2 = tf.constant([[2.], [2.]])
#
# product = tf.matmul(matrix1, matrix2)
#
# # 在一个会话中启动图
# sess = tf.Session()
#
# result = sess.run(product)
# print(result)

with tf.Session() as sess:
    while tf.device("gpu:1"):
        matrix1 = tf.constant([[3., 3.]])
        matrix2 = tf.constant([[2.], [2.]])
        product = tf.matmul(matrix1, matrix2)
        result = sess.run(product)
        print(result)
