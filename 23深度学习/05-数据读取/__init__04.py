#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import tensorflow as tf
import os


# 1 找到文件，创建列表

def csvread(filelist):
    """

    :param filelist:
    :return:
    """
    # 1 构造文件的队列
    file_queue = tf.train.string_input_producer(filelist)

    # 2 构造csv读取队列
    reader = tf.TextLineReader()
    key, value = reader.read(file_queue)

    # 3 对每行内容解码
    records = [["None"], ["None"]]
    a, b = tf.decode_csv(value, record_defaults=records)

    # 4 读取多个数据
    example_batch, label_batck = tf.train.batch([a, b], batch_size=9, num_threads=1, capacity=32)

    # return a, b
    return example_batch, label_batck


# 2 构造文件队列

# 3 构造阅读器

# 4 解码内容

# 5 批处理

if __name__ == "__main__":
    # 1 找到文件
    file_name = os.listdir("./../../data/")
    file_list = [os.path.join("./../../data/", file) for file in file_name]
    # print(file_name)

    a, b = csvread(file_list)

    with tf.Session() as sess:
        # 线程协调器、
        coord = tf.train.Coordinator()

        # 开启独缺文件的线程
        thread = tf.train.start_queue_runners(sess, coord=coord)

        # 打印读取内容
        print(sess.run([a, b]))

        # 回收子线程
        coord.request_stop()

        coord.join(thread)
