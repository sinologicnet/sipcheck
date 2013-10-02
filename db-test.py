#!/usr/bin/env python
# -~A�- coding: UTF-8 -*-
"""
  test
"""


from incl.sqlitedb import DB 


def go():

    a = DB()
    a.InsertIP("127.0.0.5")

if __name__ == '__main__':
    go()

