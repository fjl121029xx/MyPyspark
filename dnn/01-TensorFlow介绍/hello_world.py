#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy
import tensorflow as tf

q3 = tf.constant(3)
q5 = tf.constant(5)

a = tf.add(q3, q5)
print(a)

with tf.Session() as sess:
    print(sess.run(a))
