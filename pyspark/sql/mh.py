#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'


# Question = Row('pid', 'qid')

def Hello():
    print("say Hello")


def mypartiton(arr):
    list = []
    for r in arr:
        list.append({'pid': r.points[2], 'qid': r._id})
    return list


def myfile(r):
    print(r)
    if r.points :
        if len(r.points) != 3:
            return False
    else:
        return False

    return True
