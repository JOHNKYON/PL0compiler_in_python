# -*- coding:utf-8 -*-
# __author__ = "ZhaoFengbo = JOHNKYON"

tab = dict()
top = 0


def tab_insert(name, kind, val, level, adr, size):
    global top
    top += 1
    try:
        exsist = tab[name]
        return 0
    except:
        tab[name] = (top, name, kind, val, level, adr, size)


def tab_search(name):
    try:
        top = tab[name]
        return top
    except:
        return 0


def show_all():
    for ele in tab:
        print tab[ele]