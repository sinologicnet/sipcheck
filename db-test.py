#!/usr/bin/env python
# -~A�- coding: UTF-8 -*-
"""
  test
"""


from incl.sqlitedb import DB 
from incl.block import IPT

def go():

    a = DB()
    #a.InsertIP("127.0.0.5")
    #a.GetTrys("127.0.0.5")
    for ip in a.GetIPsToBlock():
        print ip[0]

    """
    print "Bloqueamos a IP"
    b = IPT()
    b.UnBlockIP("127.0.0.5")
    """
if __name__ == '__main__':
    go()

