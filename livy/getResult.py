#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import json
import requests
from bs4 import BeautifulSoup
from urllib import request
import json
import requests
import logging
import config
import time
import os

response = request.urlopen('http://bi-olap1.sm02:8999/sessions/8479/statements/24')
statements = json.loads(response.read())
print('getStatements %s' % (statements))
