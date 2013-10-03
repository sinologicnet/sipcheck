#!/usr/bin/env python
"""
  Block IP using IPTables
"""
import os
import sys
from incl.sqlitedb import DB

class IPT:

    def BlockIP(self, ip):
	#Adding iptables rule to block IP
	os.system ("iptables -A INPUT -s "+ip+" -j DROP")
        db = DB()
        db.MarkAsBlocked(ip)        

    def UnBlockIP(self, ip):
	#Deleting blocking ip rule from iptables
	os.system ("iptables -D INPUT -s "+ip+" -j DROP")
