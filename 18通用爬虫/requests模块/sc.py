#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from hbase import Hbase
from hbase.ttypes import *

# https://blog.csdn.net/qq_21153619/article/details/86502624

# thrift默认端口是9090
socket = TSocket.TSocket('192.168.100.68', 9090)
socket.setTimeout(5000)

transport = TTransport.TBufferedTransport(socket)
protocol = TBinaryProtocol.TBinaryProtocol(transport)

client = Hbase.Client(protocol)
socket.open()

print(client.getRow('scaa', '234365167-1'))
socket.close()
