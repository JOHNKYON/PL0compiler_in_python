# -*- coding:utf-8 -*-
# __author__ = "ZhaoFengbo = JOHNKYON"


import grammar
import lexial
import codecs
import tab
import gen

raw = raw_input('Please input source program file name :')
try:
    input_file = codecs.open(raw, 'rb')

    raw = input_file.read()

    lexial.length = len(raw)
    lexial.raw = raw


    grammar.program()
except StandardError:
    print 'No such file'
