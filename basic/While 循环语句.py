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



###循环使用 else 语句##################
count =0
while (count <5):
    print(count," is less than 5")
    count =count+1
else:
    print(count," is not less than 5")


