#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'


class batchGradientDescent:


    def getDate(dateSet):
        m, n = np.shape(dataSet)
        trainDate = np.ones((m, n))
        trainDate[:, :-1] = dataSet[:, :-1]
        trainLabel = dataSet[:, -1]
        return trainDate, trainLabel
