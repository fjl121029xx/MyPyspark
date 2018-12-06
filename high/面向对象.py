#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'


class Employee:
    empCount = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.empCount += 1

    def displaycount(self):
        print("Total Employee %d" % Employee.empCount)

    def displayEmployee(self):
        print("Name: ", self.name, ", Salary: ", self.salary)


class Test:
    def prt(self):
        print(self)
        print(self.__class__)


t = Test()
t.prt()

emp1 = Employee("Zara", 2000)
emp1.displayEmployee()

emp2 = Employee("Manni", 5000)
emp2.displayEmployee()
print("Total Employee %d" % Employee.empCount)

emp1.age = 7
emp1.age = 8
print(emp1.age)
del emp1.age


class Parent:
    parentAttr = 100

    def __init__(self):
        print("调用父类构造函数")

    def parentmethod(self):
        print("调用父类方法")

    def setAttr(self, attr):
        Parent.parentAttr = attr

    def getAttr(self):
        print("父类属性: ", Parent.parentAttr)

    def mymethod(self):
        print("调用父类方法")


class Child(Parent):

    def __init__(self):
        super().__init__()
        print("调用子类构造方法")

    def childmethod(self):
        print("调用子类方法")

    def mymethod(self):
        print("调用子类方法")


c = Child()
c.childmethod()
c.parentmethod()
c.setAttr(200)
c.getAttr()
c.mymethod()


class Vector:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return "Vector (%d,%d)" % (self.a, self.b)

    def __add__(self, other):
        return Vector(self.a + other.a, self.b + other.b)


v1 = Vector(2, 10)
v2 = Vector(5, -2)
print(v1 + v2)


class JustCounter:
    __secretCount = 0
    publicCount = 0

    def count(self):
        self.__secretCount += 1
        self.publicCount += 1
        print(self.__secretCount)


counter = JustCounter()
counter.count()
counter.count()

print(counter.publicCount)
