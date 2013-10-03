#!/usr/bin/env python
"""
  Block IP using IPTables
"""
import os
import sys

class IPT:

    def BlockIP(self, ip):
	#Aqui insertamos la IP en el IPtables
	os.system ("iptables -A INPUT -s "+ip+" -j DROP")

    def UnBlockIP(self, ip):
	#Aqui eliminamos la ip del IPTables
	os.system ("iptables -D INPUT -s "+ip+" -j DROP")
