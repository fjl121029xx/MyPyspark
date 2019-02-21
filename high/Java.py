#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

import jpype
import os

# pjava.jar
# jvmPath = jpype.getDefaultJVMPath()
# jvmPath = jpype.getDefaultJVMPath()
#
# print(jvmPath)
# jpype.startJVM(jvmPath)
# jpype.java.lang.System.out.println("hello world!")
# jpype.shutdownJVM()

jarpath = os.path.join(os.path.abspath('H:/pp'), 'pjava-1.0-SNAPSHOT-jar-with-dependencies.jar')
jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % jarpath)
Test = jpype.JClass('com.Test')
# 或者通过JPackage引用Test类
# com = jpype.JPackage('com')
# Test = com.Test
t = Test()
res = t.run("a")
print(res)
jpype.shutdownJVM()
