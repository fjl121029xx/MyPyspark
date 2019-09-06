#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data

# 载入MNIST数据集，如果指定地址/path/to/MNIST_data 下没有已经下载好的数据，
# 那么Tensorflow会自动下载数据

mnist = input_data.read_data_sets("/path/to/MNIST_data", one_hot=True)

# 打印Training data size：55000
print(mnist.train.num_examples)

# Validating data size: 5000
print(mnist.validation.num_examples)

# 打印Testing data size：10000
print(mnist.test.num_examples)

# 打印Example training data
print(mnist.train.images[0])

# 打印Example training data label
print(mnist.train.labels[0])

batch_size = 100

xs, ys = mnist.train.next_batch(batch_size)
# 从train的集合中选取bath_size个训练数据
print("X shape", xs.shape)
print("Y shape", ys.shape)
