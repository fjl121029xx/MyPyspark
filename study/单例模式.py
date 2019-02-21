#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
            return cls._instance


class MyCLass(Singleton):
    a = 1


m = MyCLass()
print(m.a)
