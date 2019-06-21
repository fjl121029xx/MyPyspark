#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy
import tensorflow as tf

# 以下程序实现了神经网络的前向传播过程。当声明了变量w1、w2之后，可以通过w1和w2来定义神经网络的前向传播过程并得到中间结果a和最后答案y。
#

# 声明w1、w2两个变量。这里还通过seed参数设定了随机种子
# 这样可以保证每次运行得到的结果是一样的
w1 = tf.Variable(tf.random_normal((2, 3), stddev=1, seed=1))
w2 = tf.Variable(tf.random_normal((3, 1), stddev=1, seed=1))

# 暂时将输入的特征向量定义为一个常量。注意这里x是一个1*2矩阵
x = tf.constant([[0.7, 0.9]])

# 前向传播算法获得神经网络的输出
a = tf.matmul(x, w1)
y = tf.matmul(a, w2)

with tf.Session() as sess:
    # 这里不能直接通过sess.run(y)来获取y的取值
    # 因为w1和w2都还没有运行初始化过程。以下两行分别初始化了w1和w2两个变量
    # sess.run(w1.initializer)  # 初始化w1
    # sess.run(w2.initializer)  # 初始化w2
    # 初始化所有变量
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    print(sess.run(y))
