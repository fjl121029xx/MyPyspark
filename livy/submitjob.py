#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import json
import requests
from urllib import request
import time

headers = {
    'Content-Type': 'application/json',
    'X-Requested-By': 'admin'
}
# select compare_sum(Array(report_date),food_price_amount,'ymd','0') as m from `db_yqs_b_505`.`tbl_pos_bill_food`
data = {
    'code': """
    SELECT COUNT (DISTINCT shop_name) AS `shop_name_1584011785433`,setfood_name AS `setfood_name_1584010114632`,report_date_format( cast(report_date as string),'ymd') AS `report_date_1583809351215`,__brand_id__ AS `__brand_id___1583834174151` FROM `db_yqs_b_505`.`tbl_pos_bill_food` GROUP BY `setfood_name_1584010114632`,report_date_1583809351215,__brand_id___1583834174151
   """
    ,
    'kind': "sql"
}
sid = 77984
response = requests.post("http://172.20.44.6:8999/sessions/" + str(sid) + '/statements', data=json.dumps(data),
                         headers=headers)
# response = requests.post("http://192.168.101.39:8999:8999/sessions/" + str(sid) + '/statements', data=json.dumps(data),
#                          headers=headers)
print(response.text)
id = response.json()['id']
print(id)
time.sleep(20)
response = request.urlopen('http://172.20.44.6:8999/sessions/%d/statements/%d' % (sid, id))
statements = json.loads(response.read())
print(statements)
stmt = statements['state']
print('getStatements %s' % (statements['state']))
if 'available' == stmt:
    print(statements)
    # print(statements['output']['data']['application/json']['data'][0])
