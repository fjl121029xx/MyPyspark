#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import requests as rq

res = rq.get("")

with open("a.png", "wb") as f:
    f.write(res.content)
