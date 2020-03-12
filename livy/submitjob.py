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
    SELECT sum(food_price_amount) AS `food_price_amount_1575363366863`,sum(food_realamount) AS `food_realamount_1575363371704`,sum(food_number) AS `food_number_1575365579023`,sum(food_cancel_number) AS `food_cancel_number_1575365599010`,sum(order_status) AS `order_status_1575365623819`,report_date_format( cast(report_date as string),'ymd') AS `report_date_1575363272057`,shop_name AS `shop_name_1575363281347` FROM `db_yqs_b_505`.`tbl_pos_bill_food` WHERE (((shop_name IN (  '测试-李源'  ,  '测试-南唐一'  ,  '测试-唐唐'  ,  '测试-李彦龙123'  ) ) OR (shop_name IN (  '测试-李煜'  ,  '测试门店宝-saas'  ) ))) GROUP BY report_date_1575363272057,shop_name_1575363281347 ORDER BY `report_date_1575363272057` asc,`food_price_amount_1575363366863` ASC LIMIT 1000
   """
    ,
    'kind': "sql"
}
sid = 77979
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
