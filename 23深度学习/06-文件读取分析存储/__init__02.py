#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import tensorflow as tf
import os


#
# FLAGS = tf.app.flags.FLAGS
# tf.app.flags.DEFINE_string("cifar_dir", "D:/work/cifar-10-batches-py/")


class CifarRead(object):
    """
    完成读取二进制文件，写进tfrecords，读取tfrecords
    """

    def __init__(self, filelist):
        # 文件列表
        self.file_list = filelist
        #
        self.height = 32
        self.width = 32
        self.channel = 3
        self.label_bytes = 1
        self.image_bytes = self.height * self.width * self.channel
        self.bytes = self.image_bytes + self.label_bytes

    def read_and_decode(self):
        # 1 构造文件队列
        file_queue = tf.train.string_input_producer(self.file_list)

        # 2 读取器
        reader = tf.FixedLengthRecordReader(self.bytes)
        k, v = reader.read(file_queue)

        # 3 解码
        label_image = tf.decode_raw(v, tf.uint8)

        # print(label_image)
        # 4 分割标签值 特征值
        label = tf.slice(label_image, [0], [self.label_bytes])
        image = tf.slice(label_image, [self.label_bytes], [self.image_bytes])

        # 5 对图片的特征数据进行形状的改变
        image_reshape = tf.reshape(image, [self.height, self.width, self.channel])
        # print(label, image_reshape)

        # 6 批处理数据
        label_batch, image_batch = tf.train.batch([label, image_reshape], batch_size=10, num_threads=1, capacity=10)
        return label_batch, image_batch


# 二进制文件格式


if __name__ == "__main__":
    # 1 找到文件
    file_name = os.listdir("D:/work/cifar-10-batches-py/")
    print(file_name)
    file_list = [os.path.join("D:/work/cifar-10-batches-py/", file) for file in file_name if file.startswith("data")]

    print(file_list)
    cf = CifarRead(file_list)

    label_batch, image_batch = cf.read_and_decode()
    with tf.Session() as sess:
        # 线程协调器、
        coord = tf.train.Coordinator()

        # 开启独缺文件的线程
        thread = tf.train.start_queue_runners(sess, coord=coord)

        # 打印读取内容
        print(sess.run([label_batch,image_batch]))

        # 回收子线程
        coord.request_stop()

        coord.join(thread)
