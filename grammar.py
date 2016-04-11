# -*- coding:utf-8 -*-
# __author__ = "ZhaoFengbo = JOHNKYON"
import lexial
import codecs
import tab
import gen
import stack


addr_begin = 0
adr = 3
size = 0
flag = True
flag2 = True
procedure_dict = dict()

# 扫描下一个符号
def nextsym():
    lexial.getsysm()


def error(information):
    print 'error at line' + str(lexial.line_counter)
    print information
    nextsym()


def constDefine(level):
    global adr
    global size
    if lexial.symbol == 20:
        name = lexial.token
        nextsym()
        if lexial.symbol == 32:
            nextsym()
            if lexial.symbol == 21:
                value = lexial.token
                nextsym()
                tab.tab_insert(name, 'constant', value, level, 0, 0)
            else:
                error('= 后应为数')
                lexial.symbol = 21
        else:
            error('标识符后应为 =')
            lexial.symbol = 32
    else:
        error('const后应为标识符')
        lexial.symbol == 20


# 常量说明
def constClaim(level):
    constDefine(level)
    while lexial.symbol == 28:
        nextsym()
        constDefine(level)
    if lexial.symbol == 29:
        nextsym()
    else:
        error('漏掉分号')
        lexial.symbol == 29


# 变量说明
def varClaim(level):
    global adr
    global size
    if lexial.symbol == 20:
        name = lexial.token
        value = ''
        tab.tab_insert(name, 'variable', value, level, adr, 0)
        stack.insert_data_stack(value)
        adr += 1
        size += 1
        nextsym()
        while lexial.symbol == 28:
            nextsym()
            if lexial.symbol == 20:
                name = lexial.token
                value = ''
                tab.tab_insert(name, 'variable', value, level, adr, 0)
                adr += 1
                size += 1
                nextsym()
            else:
                error(',后应为标识符')
                lexial.symbol == 20
        if lexial.symbol == 29:
            nextsym()
        else:
            error('漏掉分号')
            lexial.symbol == 29
    else:
        error('var后应为标识符')
        lexial.symbol == 20


# 过程说明
def procClaim(level):
    global size
    global adr
    global procedure_dict
    if lexial.symbol == 20:
        name = lexial.token
        procedure_dict[name] = gen.top+2
        nextsym()
        if lexial.symbol == 29:
            nextsym()
        else:
            error('漏掉分号')
            lexial.symbol == 29
        subPro(level)
        adr -= (size + 3)
        tab.tab_insert(name, 'procedure', '', level, adr, size)
        adr += 1
        if lexial.symbol == 29:
            nextsym()
            while lexial.symbol == 8:
                nextsym()
                procClaim(level)
        else:
            error('漏掉分号')
            lexial.symbol == 29


# 项
def item(level):
    factor(level)
    while lexial.symbol == 24 or lexial.symbol == 25:
        mop = lexial.symbol
        nextsym()
        factor(level)
        gen.OPR(mop-20)


# 因子
def factor(level):
    if lexial.symbol == 20:
        word = tab.tab_search(lexial.token)
        if word != 0:
            if word[2] == 'constant':
                gen.LIT(word[3])
            else:
                gen.LOD(level-word[4], word[5])
        nextsym()
    elif lexial.symbol == 21:
        gen.LIT(lexial.token)
        nextsym()
    elif lexial.symbol == 26:
        nextsym()
        express(level)
        if lexial.symbol == 27:
            nextsym()
        else:
            error('漏右括号')
            lexial.symbol == 27
    else:
        error('应为左括号')
        lexial.symbol == 20


# 表达式
def express(level):
    if lexial.symbol == 22 or lexial.symbol == 23:      # 如果有加减
        adop = lexial.symbol
        nextsym()
        item(level)
        if adop == 23:
            gen.OPR(3)
        while lexial.symbol == 22 or lexial.symbol == 23:
            nextsym()
            item(level)
    else:
        item(level)
    while lexial.symbol == 22 or lexial.symbol == 23:
        adop = lexial.symbol
        nextsym()
        item(level)
        if adop == 22:
            gen.OPR(2)
        else:
            gen.OPR(3)


# 条件
def condition(level):
    express(level)
    if lexial.symbol == 11:
        nextsym()
        express(level)
    elif lexial.symbol == 32 or lexial.symbol == 33 or lexial.symbol == 34 or lexial.symbol == 35 or lexial.symbol == 36 or lexial.symbol == 37:
        symbol = lexial.symbol
        nextsym()
        express(level)
        if symbol == 33:
            gen.OPR(9)
    else:
        error('应为关系运算符')
        lexial.symbol == 32


# 赋值语句
def evaluation(level):
    if lexial.symbol == 31:
        nextsym()
        express(level)
    else:
        error('应为:=')
        lexial.symbol == 31


# 条件语句
def condi_sen(level):
    condition(level)
    addr1 = gen.top+1
    gen.JPC(addr1)
    if lexial.symbol == 4:
        nextsym()
        sentence(level)
        if lexial.symbol == 5:
            gen.Pcode[addr1][2] = gen.top
            nextsym()
            sentence(level)
    else:
        error('应为then')
        lexial.symbol == 4


# 当型循环语句
def do_while(level):
    addr2 = gen.top+1
    condition(level)
    addr3 = gen.top+1
    gen.JPC(addr3)
    if lexial.symbol == 10:
        nextsym()
        sentence(level)
        gen.JPC(addr2)
        gen.Pcode[addr3][2] = gen.top+2
    else:
        error('应为do')
        lexial.symbol == 10


# 过程调用语句
def call_sen(level):
    if lexial.symbol == 20:
        name = lexial.token
        row = tab.tab_search(name)
        if row != 0:
            lev = int(row[4]) - level
            addr = procedure_dict[name]
            gen.CAL(lev, addr)
        else:
            error('标识符未说明')
            lexial.symbol == 20
        nextsym()
    else:
        error('应为标识符')
        lexial.symbol == 20


# 读语句
def read_sen(level):
    if lexial.symbol == 26:
        nextsym()
        if lexial.symbol == 20:
            row = tab.tab_search(lexial.token)
            lev = row[4]
            adr = row[5]
            gen.RED(level-int(lev), adr)
            nextsym()
            while lexial.symbol == 28:
                nextsym()
                if lexial.symbol == 20:
                    nextsym()
                else:
                    error('应为标识符')
            if lexial.symbol == 27:
                nextsym()
            else:
                error('漏右括号')
                lexial.symbol == 28
        else:
            error('应为标识符')
            lexial == 20
    else:
        error('应为左括号')
        lexial.symbol == 26


# 写语句
def write_sen(level):
    if lexial.symbol == 26:
        nextsym()
        if lexial.symbol == 20:
            row = tab.tab_search(lexial.token)
            gen.LOD(row[4] - level, row[5])
            gen.WRT()
            nextsym()
            while lexial.symbol == 28:
                nextsym()
                if lexial.symbol == 20:
                    row = tab.tab_search(lexial.token)
                    gen.LOD(row[4] - level, row[5])
                    gen.WRT()
                    nextsym()
                elif lexial.symbol == 21:
                    nextsym()
                    if lexial.symbol == 27:
                        nextsym()
                    else:
                        error('漏右括号')
                        lexial.symbol == 27
                else:
                    error('应为标识符或整数')
                    lexial.symbol == 20
            if lexial.symbol == 27:
                nextsym()
        elif lexial.symbol == 21:
            nextsym()
            while lexial.symbol == 28:
                nextsym()
                if lexial.symbol == 20:
                    nextsym()
                    if lexial.symbol == 27:
                        nextsym()
                        gen.WRT()
                    else:
                        error('漏右括号')
                        lexial.symbol == 27
                elif lexial.symbol == 21:
                    nextsym()
                    if lexial.symbol == 27:
                        nextsym()
                    else:
                        error('漏右括号')
                        lexial.symbol == 27
                else:
                    error('应为标识符或整数')
                    lexial.symbol == 20
        else:
            error('应为标识符或整数')
            lexial.symbol == 20
    else:
        error('应为左括号')
        lexial.symbol == 26


# 复合语句
def complex(level):
    global flag
    global addr_begin
    flag2 = True
    if level == 0 and flag:
        flag = False
        gen.Pcode[0][2] = gen.top
    sentence(level)
    while lexial.symbol == 29:
        nextsym()
        if lexial.symbol == 2:
            pass
        else:
            sentence(level)
    if lexial.symbol == 2:
        nextsym()
    else:
        print lexial.token
        print lexial.symbol
        error('应为end')
        lexial.symbol == 2


# 重复语句
def repeat(level):
    addr4 = gen.top+1
    sentence(level)
    while lexial.symbol == 30:
        nextsym()
        sentence(level)
    if lexial.symbol == 14:
        nextsym()
        condition(level)
        gen.JPC(addr4)
    else:
        error('漏until')
        lexial.symbol == 14


# 语句
def sentence(level):
    if lexial.symbol == 20:     # 赋值语句
        var = tab.tab_search(lexial.token)
        adr = var[5]
        nextsym()
        evaluation(level)
        gen.STO(level - int(var[4]), adr)
    elif lexial.symbol == 3:      # 条件语句
        nextsym()
        condi_sen(level)
    elif lexial.symbol == 9:      # 当型循环语句
        nextsym()
        do_while(level)
    elif lexial.symbol == 12:      # 过程调用语句
        nextsym()
        call_sen(level)
    elif lexial.symbol == 15:     # 读语句
        nextsym()
        read_sen(level)
    elif lexial.symbol == 16:     # 写语句
        nextsym()
        write_sen(level)
    elif lexial.symbol == 1:      # 复合语句
        nextsym()
        complex(level)
    elif lexial.symbol == 13:      # 重复语句
        nextsym()
        repeat(level)
    elif lexial.symbol == 29:
        pass
    elif lexial.symbol == 0:
        if lexial.symbol == 41:
            nextsym()
        else:
            error('应有语句')
        pass


def subPro(level):
    global adr
    global size
    global flag2
    private_adr = adr
    level += 1
    adr = 3
    if flag2:
        pass
        flag2 = False
    else:
        gen.JMP(gen.top+2)
    mysize = 0
    if lexial.symbol == 6:  # 常量声明
        nextsym()
        constClaim(level)
    if lexial.symbol == 7:  # 变量声明
        nextsym()
        varClaim(level)
        mysize = size
        size = 0
    if lexial.symbol == 8:  # 过程声明
        RA = gen.top
        SL = private_adr + 1
        nextsym()
        procClaim(level)
    gen.INT(mysize+3)
    sentence(level)
    gen.OPR(0)
    adr = 3


def program():
    global addr_begin
    global adr
    adr = 3
    level = -1
    gen.JMP(addr_begin)
    nextsym()
    subPro(level)
    gen.gen_write()

    if lexial.symbol == 41:
        exit()
    else:
        error('程序不完整')
        exit()

