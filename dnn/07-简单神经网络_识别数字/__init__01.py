#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

is_train = False


def full_connected():
    # 获取真实数据
    mnist = input_data.read_data_sets("D:/work/mnist/", one_hot=True)

    # 1\ 数据占位符
    with tf.variable_scope("data"):
        x = tf.placeholder(tf.float32, [None, 784])
        y_true = tf.placeholder(tf.int32, [None, 10])

    # 2\ 建立全连接层的神经网络
    with tf.variable_scope("fc_model"):
        # 随机初始化权重和偏置
        weight = tf.Variable(tf.random_normal([784, 10], mean=0.0, stddev=1.0), name="weight")

        bias = tf.Variable(tf.constant(0.0, shape=[10]))

        # 预测输出结果
        y_predict = tf.matmul(x, weight) + bias

    # 3\ 求出所有样本的损失，然后求平均值
    with tf.variable_scope("scro_cross"):
        # 平均交叉熵损失
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_true, logits=y_predict))

    # 4\ 梯度下降
    with tf.variable_scope("computes"):
        train_op = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

    # 5\ 计算准确率
    with tf.variable_scope("accur"):
        equal_list = tf.equal(tf.argmax(y_true, 1), tf.argmax(y_predict, 1))

        accuracy = tf.reduce_mean(tf.cast(equal_list, tf.float32))

    # 收集变量
    tf.summary.scalar("loss", loss)
    tf.summary.scalar("accuracy", accuracy)
    # 收集高纬度变量
    tf.summary.histogram("weight", weight)
    tf.summary.histogram("bias", bias)

    # 初始化变量
    init_op = tf.global_variables_initializer()

    # 定义合并变量
    merged = tf.summary.merge_all()

    # 创建一个saver
    saver = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(init_op)
        # 建立events文件
        file_writer = tf.summary.FileWriter("./summary/", graph=sess.graph)

        if is_train == True:
            # 迭代训练
            for i in range(2000):
                # 取出特征值，目标值
                m_x, m_y = mnist.train.next_batch(50)

                # 运行
                sess.run(train_op, feed_dict={x: m_x, y_true: m_y})

                # 写入每一步训练的值
                summ = sess.run(merged, feed_dict={x: m_x, y_true: m_y})
                # 保存模型
                file_writer.add_summary(summ, i)

                print("训练%d次,准确率为%f" % (i, sess.run(accuracy, feed_dict={x: m_x, y_true: m_y})))
            # 保存模型
            saver.save(sess, "./sa/fc_model")
        else:
            # 加载模型
            saver.restore(sess, "./sa/fc_model")
            # 预测
            for i in range(100):
                # 每次测试一张图片
                x_test, y_test = mnist.test.next_batch(1)
                print("第%d张图片，手写数字目标是%d，预测结果是：%d" % (
                    i,
                    tf.argmax(y_test, 1).eval(),
                    tf.argmax(sess.run(y_predict, feed_dict={x: x_test, y_true: y_test}), 1).eval()
                ))

    return None


if __name__ == "__main__":
    full_connected()
