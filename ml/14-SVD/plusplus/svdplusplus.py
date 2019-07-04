#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy as np
import random
import tensorflow as tf
import re


# https://blog.csdn.net/akiyamamio11/article/details/79313339

class SVDPP:
    def __init__(self, mat, K=20):
        self.mat = np.array(mat)
        self.K = K
        self.bi = {}
        self.bu = {}
        self.qi = {}
        self.pu = {}
        self.avg = np.mean(self.mat[:, 2])
        self.y = {}
        self.u_dict = {}
        for i in range(self.mat.shape[0]):
            uid = self.mat[i, 0]
            iid = self.mat[i, 1]
            self.u_dict.setdefault(uid, [])
            self.u_dict[uid].append(iid)
            self.bi.setdefault(iid, 0)
            self.bu.setdefault(uid, 0)
            self.qi.setdefault(iid, np.random.random((self.K, 1)) / 10 * np.sqrt(self.K))
            self.pu.setdefault(uid, np.random.random((self.K, 1)) / 10 * np.sqrt(self.K))
            self.y.setdefault(iid, np.zeros((self.K, 1)) + .1)

    def predict(self, uid, iid):
        self.bi.setdefault(iid, 0)
        self.bu.setdefault(uid, 0)
        self.qi.setdefault(iid, np.zeros((self.K, 1)))
        self.pu.setdefault(uid, np.zeros((self.K, 1)))
        self.y.setdefault(uid, np.zeros((self.K, 1)))
        self.u_dict.setdefault(uid, [])
        u_impl_prf, sqrt_Nu = self.getY(uid, iid)
        rating = self.avg + self.bi[iid] + self.bu[uid] + np.sum(self.qi[iid] * (self.pu[uid] + u_impl_prf))
        if rating > 5:
            rating = 5
        if rating < 1:
            rating = 1
        return rating

    # 计算sqrt_Nu和∑yj
    def getY(self, uid, iid):
        Nu = self.u_dict[uid]
        I_Nu = len(Nu)
        sqrt_Nu = np.sqrt(I_Nu)
        y_u = np.zeros((self.K, 1))
        if I_Nu == 0:
            u_impl_prf = y_u
        else:
            for i in Nu:
                y_u += self.y[i]
            u_impl_prf = y_u / sqrt_Nu
        return u_impl_prf, sqrt_Nu

    def train(self, steps=30, gamma=0.04, Lambda=0.15):
        print('train data size', self.mat.shape)
        for step in range(steps):
            print('step ', step + 1, ' is running')
            KK = np.random.permutation(self.mat.shape[0])
            rmse = 0.0
            for i in range(self.mat.shape[0]):
                j = KK[i]
                uid = self.mat[j, 0]
                iid = self.mat[j, 1]
                rating = self.mat[j, 2]
                predict = self.predict(uid, iid)
                u_impl_prf, sqrt_Nu = self.getY(uid, iid)
                eui = rating - predict
                rmse += eui ** 2
                self.bu[uid] += gamma * (eui - Lambda * self.bu[uid])
                self.bi[iid] += gamma * (eui - Lambda * self.bi[iid])
                self.pu[uid] += gamma * (eui * self.qi[iid] - Lambda * self.pu[uid])
                self.qi[iid] += gamma * (eui * (self.pu[uid] + u_impl_prf) - Lambda * self.qi[iid])
                for j in self.u_dict[uid]:
                    self.y[j] += gamma * (eui * self.qi[j] / sqrt_Nu - Lambda * self.y[j])
            gamma = 0.93 * gamma
            print('rmse is ', np.sqrt(eui * self.qi[j] / sqrt_Nu - Lambda * self.y[j]))

    def test(self, test_data):
        test_data = np.array(test_data)
        print('test data size ', test_data.shape)
        rmse = 0.0
        for i in range(test_data.shape[0]):
            uid = test_data[i, 0]
            iid = test_data[i, 1]
            rating = test_data[i, 2]
            eui = rating - self.predict(uid, iid)
            rmse += eui ** 2
        print('rmse of test data is ', np.sqrt(rmse / test_data.shape[0]))


def getMLData():
    f = open('u1.base')
    lines = f.readlines()
    f.close()

    data = []
    for line in lines:
        list = re.split('\t|\n', line)
        if int(list[2]) != 0:
            data.append([int(i) for i in list[:3]])
    train_data = data
    f = open('u1.test', 'r')
    lines = f.readlines()
    f.close()
    data = []
    for line in lines:
        list = re.split('\t|\n', line)
        if int(list[2] != 0):
            data.append([int(i) for i in list[:3]])
    test_data = data
    return train_data, test_data


train_data, test_data = getMLData()
a = SVDPP(train_data, 3)
a.train()
a.test(test_data)
