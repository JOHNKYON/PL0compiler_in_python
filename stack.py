# -*- coding:utf-8 -*-
# __author__ = "ZhaoFengbo = JOHNKYON"

data_stack = list()
data_top = 0

adr = 0


def insert_data_stack(value):
    global data_top
    data_stack.append(value)
    data_top += 1