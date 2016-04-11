# -*- coding:utf-8 -*-
# __author__ = "ZhaoFengbo = JOHNKYON"

from __future__ import absolute_import
import codecs


input_file = codecs.open("source1.txt", 'rb')


line_counter = 0        # 行数计数器
position = -1           # 当前字符指针
token = ''              # 单词
length = 0              # 源文件长度
raw = ''                # 源文件
ch = ''
symbol = -1


# 重置token
def clearToken():
    global token
    token = ''


def isSpace():
    global ch
    return ch == ' '


def isNewLine():
    global ch
    return ch == '\n' or ch == '\r'


def isTab():
    global ch
    return ch == '\t'


def isColon():
    global ch
    return ch == ':'


def isComma():
    global ch
    return ch == ','


def isSemi():
    global ch
    return ch == ';'


def isEqu():
    global ch
    return ch == '='


def isPlus():
    global ch
    return ch == '+'


def isMinus():
    global ch
    return ch == '-'


def isDivid():
    global ch
    return ch == '/'


def isStar():
    global ch
    return ch == '*'


def isLpar():
    global ch
    return ch == '('


def isRpar():
    global ch
    return ch == ')'


def isLess():
    global ch
    return ch == '<'


def isGreater():
    global ch
    return ch == '>'


def isQuote():
    global ch
    return ch == '\''


def isLbrace():
    global ch
    return ch == '{'


def isRbrace():
    global ch
    return ch == '}'


def isDot():
    global ch
    return ch == '.'


# 将当前字符加入当前token
def catToken():
    global token
    global ch
    token += ch


# 读取下一字符
def getChar():
    global raw
    global token
    global position
    global ch
    # print position
    position += 1
    if position >= length:
        ch = ''
    else:
        ch = raw[position]


# 将字符指针后退一个字符
def retract():
    global raw
    global position
    global ch
    position -= 1
    ch = raw[position]


# 将token中的字符串转换成整数，返回这个值
def transNum():
    global token
    return int(token)


def reserver():
    global token
    if token == 'begin':
        return 1
    elif token == 'end':
        return 2
    elif token == 'if':
        return 3
    elif token == 'then':
        return 4
    elif token == 'else':
        return 5
    elif token == 'const':
        return 6
    elif token == 'var':
        return 7
    elif token == 'procedure':
        return 8
    elif token == 'while':
        return 9
    elif token == 'do':
        return 10
    elif token == 'odd':
        return 11
    elif token == 'call':
        return 12
    elif token == 'repeat':
        return 13
    elif token == 'until':
        return 14
    elif token == 'read':
        return 15
    elif token == 'write':
        return 16
    else:
        return 0


def error(str):
    global line_counter
    global ch
    print ch
    print('error at %d line', line_counter)
    print str


def getsysm():
    global line_counter
    global position
    global ch
    global symbol
    clearToken()
    getChar()
    while isSpace() or isNewLine() or isTab():
        if isNewLine():
            line_counter += 1
            position_counter = 0
        getChar()

    if ch == '':        # 文件结尾
        symbol = 0

    # 如果是字母
    elif ch.isalpha():
        while ch.isalnum():
            catToken()
            getChar()
        retract()
        result_value = reserver()
        if result_value == 0:
            symbol = 20         # 'IDSY'
        else:
            symbol = result_value

    # 如果是数字
    elif ch.isdigit():
        while ch.isdigit():
            catToken()
            getChar()
        retract()
        num = transNum()
        symbol = 21             # 'INTSY'

    # 如果是冒号
    elif isColon():
        getChar()
        if isEqu():
            symbol = 31         # 'ASSIGNSY'
        else:
            retract()
            symbol = 30         # 'COLONSY'

    # 如果是小于
    elif isLess():
        getChar()
        if isEqu():
            symbol = 35         # 'LESEQSY'
        elif isGreater():
            symbol = 33         # 'NEQUSY'
        else:
            retract()
            symbol = 34         # 'LESSSY'

    # 如果是大于
    elif isGreater():
        getChar()
        if isEqu():
            symbol = 37         # 'GREEQSY'
        else:
            retract()
            symbol = 36         # 'GRESY'

    elif isEqu():
        symbol = 32             # 'EQUSY'
    elif isPlus():
        symbol = 22             # 'PLUSSY'
    elif isMinus():
        symbol = 23             # 'MINUSSY'
    elif isStar():
        symbol = 24             # 'STARSY'
    elif isLpar():
        symbol = 26             # 'LPARSY'
    elif isRpar():
        symbol = 27             # 'RPARSY'
    elif isComma():
        symbol = 28             # 'COMMASY'
    elif isSemi():
        symbol = 29             # 'SEMISY'
    elif isDivid():
        symbol = 25
    elif isQuote():
        symbol = 38
    elif isLbrace():
        symbol = 39
    elif isRbrace():
        symbol = 40
    elif isDot():
        symbol = 41

    else:
        error(str)
        return 0

# test
'''count = 0
raw = input_file.read()
print len(raw)
while count < 10:
    getsysm()

    print token

    print symbol
    count += 1
input_file.close()
output_file.close()'''