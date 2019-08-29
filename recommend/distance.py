#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

from numpy import *
from numpy import linalg as la


def euclid_sim(in_a, in_b):
    return 1.0 / (1.0 + la.norm(in_a - in_b))


def pears_sim(in_a, in_b):
    if len(in_a) < 3:
        return 1.0
    return 0.5 + 0.5 * corrcoef(in_a, in_b, rowvar=0)[0][1]


def cos_sim(in_a, in_b):
    # print('in_a', in_a, 'in_b', in_b)
    num = float(in_a.T * in_b)
    denom = la.norm(in_a) * la.norm(in_b)
    if denom == 0:
        return 0.0
    return 0.5 + 0.5 * (num / denom)
