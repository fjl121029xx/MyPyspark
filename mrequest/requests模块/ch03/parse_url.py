#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'the king of north'
#
import numpy as np
import pandas as pd

import requests

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}


def _parse_url(url):
    response = requests.get(url, headers=headers, timeout=3)
    assert response.status_code == 200
    return response.content.decode()


def parse_url(url):
    try:
        html_str = _parse_url(url)
    except:
        html_str = None

    return html_str


if __name__ == '__main__':
    url = 'http://www.baidu.com'
    print(parse_url(url))
