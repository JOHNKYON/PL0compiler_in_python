# -*- coding:utf-8 -*-
# __author__ = "ZhaoFengbo = JOHNKYON"

import codecs

top = -1

output_file = codecs.open("Pcode.txt", 'wb')


Pcode = list()


def LIT(a):
    global top
    a = str(a)
    # output_file.write('LIT 0 , ' + a + '\n')
    row = ['LIT', 0, a]
    Pcode.append(row)
    top += 1


def OPR(a):
    global top
    global top
    # output_file.write('OPR 0 , ' + a + '\n')
    row = ['OPR', 0, a]
    Pcode.append(row)
    top += 1


def LOD(lev, addr):
    global top
    lev = str(lev)
    addr = str(addr)
    # output_file.write('LOD ' + lev + ' , ' + addr + '\n')
    row = ['LOD', lev, int(addr)]
    Pcode.append(row)
    top += 1


def STO(level, a):
    global top
    a = str(a)
    # output_file.write('STO 0 , ' + a + '\n')
    row = ['STO', level, int(a)]
    Pcode.append(row)
    top += 1


def CAL(level, a):
    global top
    a = str(a)
    # output_file.write('CAL 0 , ' + a + '\n')
    row = ['CAL', level, a]
    Pcode.append(row)
    top += 1


def INT(a):
    global top
    a = str(a)
    # output_file.write('INT 0 , ' + a + '\n')
    row = ['INT', 0, int(a)]
    Pcode.append(row)
    top += 1


def JMP(a):
    global top
    a = str(a)
    # output_file.write('JMP 0 , ' + a + '\n')
    row = ['JMP', 0, a]
    Pcode.append(row)
    top += 1


def JPC(a):
    global top
    a = str(a)
    # output_file.write('JPC 0 , ' + a + '\n')
    row = ['JPC', 0, int(a)]
    Pcode.append(row)
    top += 1


def RED(level, a):
    global top
    a = str(a)
    # output_file.write('RED 0 , ' + a + '\n')
    row = ['RED', level, int(a)]
    Pcode.append(row)
    top += 1


def WRT():
    global top
    # output_file.write('WRT 0 , ' + a + '\n')
    row = ['WRT', 0, 0]
    Pcode.append(row)
    top += 1


def gen_write():
    count = 0
    for ele in Pcode:
        output_file.write(str(count)+ '\t' + ele[0] + '\t' + str(ele[1]) + '\t' + str(ele[2]) + '\n')
        count += 1
