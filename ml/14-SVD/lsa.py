#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy
import tensorflow as tf
from matplotlib import pyplot as plt
from numpy import zeros
from numpy.linalg import svd
from math import log
from numpy import asarray, sum

titles = ["The Neatest Little Guide to Stock Market Investing",
          "Investing For Dummies, 4th Edition",
          "The Little Book of Common Sense Investing: The Only Way to \
          Guarantee Your Fair Share of Stock Market Returns",
          "The Little Book of Value Investing",
          "Value Investing: From Graham to Buffett and Beyond",
          "Rich Dad's Guide to Investing: What the Rich Invest in,\
          That the Poor and the Middle Class Do Not!",
          "Investing in Real Estate, 5th Edition",
          "Stock Investing For Dummies",
          "Rich Dad's Advisors: The ABC1s of Real Estate Investing:\
          The Secrets of Finding Hidden Profits Most Investors Miss"
          ]
stopwords = ['and', 'edition', 'for', 'in', 'little', 'of', 'the ', 'to']
ignorechars = ''',:'!'''


class LSA(object):
    def __init__(self, stopwords, ignorechars):
        self.stopwords = stopwords
        self.ignorechars = ignorechars
        self.wdict = {}
        self.dcount = 0

    def parse(self, doc):
        words = doc.split()
        for w in words:
            w = w.lower().translate(self.ignorechars)
            if w in self.stopwords:
                continue
            elif w in self.wdict:
                self.wdict[w].append(self.dcount)
            else:
                self.wdict[w] = [self.dcount]
        self.dcount += 1

    def build(self):
        self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
        self.keys.sort()
        self.A = zeros([len(self.keys), self.dcount])
        for i, k in enumerate(self.keys):
            for d in self.wdict[k]:
                self.A[i, d] += 1

    def calc(self):
        self.U, self.S, self.Vt = svd(self.A)

    def TFIDF(self):
        WordsPerDoc = sum(self.A, axis=0)
        DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
        rows, cols = self.A.shape
        for i in range(rows):
            for j in range(cols):
                self.A[i, j] = (self.A[i, j] / WordsPerDoc[j]) * log(float(cols) / DocsPerWord[i])

    def printA(self):
        print('Here is the count matrix')
        print(self.A)

    def printSVD(self):
        print('Here are the singular values')
        print(self.S)
        print('Here are first 3 colums of the U matrix')
        print(-1 * self.U[:, 0:2])

        x = self.U[:, 0:2][0, :]
        print(x)
        y = self.U[:, 0:2][1, :]
        print(y)

        plt.scatter(x, y)
        plt.show()

        print('Here are the first 3 rows of the Vt matrix')
        print(-1 * self.Vt[0:2, :])


mylsa = LSA(stopwords, ignorechars)
for t in titles:
    mylsa.parse(t)

mylsa.build()
mylsa.printA()
mylsa.calc()
mylsa.printSVD()
