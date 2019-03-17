#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import tensorflow as tf
import os


# 图片识别

def picread(filelist):
    """
    读取图片并转换成张量
    :param filelist:
    :return: 每张图片的张量
    """
    # 1 文件列表
    file_queue = tf.train.string_input_producer(filelist)

    # 2 构造图像阅读器
    reader = tf.WholeFileReader()

    key, value = reader.read(file_queue)

    # 3 解码
    image = tf.image.decode_jpeg(value)
    print(image)

    # 5 处理图片大小
    image_resize = tf.image.resize_images(image, size=[200, 200])
    image_resize.set_shape(shape=[200, 200, 3])
    print(image_resize)
    # 5 批处理
    image_batch = tf.train.batch([image_resize], batch_size=5, num_threads=1, capacity=5)

    return image_batch


if __name__ == "__main__":
    # 1 找到文件
    file_name = os.listdir("./../../data/dog/")
    file_list = [os.path.join("./../../data/dog/", file) for file in file_name]
    # print(file_name)

    image_resize = picread(file_list)

    with tf.Session() as sess:
        # 线程协调器、
        coord = tf.train.Coordinator()

        # 开启独缺文件的线程
        thread = tf.train.start_queue_runners(sess, coord=coord)

        # 打印读取内容
        print(sess.run([image_resize]))

        # 回收子线程
        coord.request_stop()

        coord.join(thread)
