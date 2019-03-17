#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import tensorflow as tf
import os

# tensorflow 实现线性回归


# 学习率

# 1\定义命令行参数
# 2\程序当中获取定义命令行参数
tf.app.flags.DEFINE_integer("max_step", 100, "模型训练的步数")
tf.app.flags.DEFINE_string("model_dir", " ", "文件保存路径")

# 定义获取参数名字
FLAGS = tf.app.flags.FLAGS
#
def myregression():
    """
    自定义线性回归
    :return:
    """
    # 1、准备数据，x 特征值 [100,10] y 目标值[100]
    x = tf.random_normal([100, 1], mean=1.75, stddev=0.5, name="x_data")

    # 矩阵相乘
    y_true = tf.matmul(x, [[0.7]]) + 0.8

    # 2 建立线性回归模型
    # 随机给一个权重和偏置的值，让他去计算损失，然后再当前状态下优化
    # 用变量定义才能优化
    # trainable参数：制定这个变量能跟着梯度下降一起优化
    weight = tf.Variable(tf.random_normal([1, 1], mean=0.0, stddev=1.0), name="w", trainable=True)
    bias = tf.Variable(0.0, name="b")

    y_predict = tf.matmul(x, weight) + bias

    # 3 建立损失函数
    loss = tf.reduce_mean(tf.square(y_true - y_predict))

    # 4 梯度下降优化损失
    train_op = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

    # 第一步 收集变量
    tf.summary.scalar("loss2", loss)
    tf.summary.histogram("wi", weight)
    tf.summary.histogram("wb", bias)

    # 合并
    merged = tf.summary.merge_all()

    # 5 初始化
    init_op = tf.global_variables_initializer()
    # 定义一个保存模型的值
    server = tf.train.Saver()

    # 5 通过会话开始运行
    with tf.Session() as sess:
        # 初始化变量
        sess.run(init_op)

        # 打印 随机
        print("随机初始化的参数为：%f,偏置为：%f" % (weight.eval(), bias.eval()))

        if os.path.exists("a"):
            server.restore(sess, "a")

        # 循环训练 运行优化
        for i in range(FLAGS.max_step):
            sess.run(train_op)
            suma = sess.run(merged)

            filewriter = tf.summary.FileWriter("s", graph=sess.graph)
            filewriter.add_summary(suma, i)

            print("第%d随机初始化的参数为：%f,偏置为：%f" % (i, weight.eval(), bias.eval()))

        server.save(sess, "a")

    return None


if __name__ == "__main__":
    myregression()
