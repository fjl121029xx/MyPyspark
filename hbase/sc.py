#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import sensorsanalytics

# 从神策分析配置页面中获取数据接收的 URL
SA_SERVER_URL = 'https://datax-api.huatu.com/sa?project=default'

# 初始化一个 Consumer，用于数据发送
# DefaultConsumer 是同步发送数据，因此不要在任何线上的服务中使用此 Consumer
consumer = sensorsanalytics.DefaultConsumer(SA_SERVER_URL)
# 使用 Consumer 来构造 SensorsAnalytics 对象
sa = sensorsanalytics.SensorsAnalytics(consumer)

# 记录用户登录事件
distinct_id = 'hahah233'
properties = {
    # 用户性别属性（Sex）为男性
    'Sex': 'Male',
    # 用户等级属性（Level）为 VIP
    'UserLevel': 'Elite VIP',
}

# 设置用户属性
sa.profile_set(distinct_id, properties, is_login_id=True)
sa.close()
