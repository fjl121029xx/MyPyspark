#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'

###while
numbers = [12, 37, 5, 42, 8, 3]
even = []
odd = []
while len(numbers) > 0:
    number = numbers.pop()
    if (number % 2 == 0):
        even.append(number)
    else:
        odd.append(number)

print(even)
print(odd)
