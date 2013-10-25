#!/usr/bin/python -B
# -*- coding: utf-8 -*-

import configOptionsParser,iptablesController,sqlitedb,ignoreList
import time,sys,os,re


class SIPCheck(object):
    def __init__(self):

	# Inicialize sipcheck configuration file
	self.config=configOptionsParser.ConfigFile("sipcheck.conf")

	# Initialize iptables object with the ip list that we are going to ban
	self.iptables=iptablesController.IPTables()

	# Initialize database object to load ip list to ban
	self.db=sqlitedb.DB()

	# Inicialize list of host and networks to ignore
	self.ignoreList=ignoreList.IgnoreList("sipcheck.ignore")

	#Process Asterisk message file...
	while True:
	    ip=self.processFile()
	    if not self.ignoreList.isInList(ip):
		tries=self.db.InsertIP(ip)
		if tries > self.config.minticks and tries <= self.config.minticks+1 :
		    print "Baneamos la IP",ip
#		    self.iptables.banip(ip)



    def processFile(self):
	''' Method to read last lines of the message file and returns the attacker ip address '''
	self.file = open(self.config.messagefile, 'r')
	st_results = os.stat(self.config.messagefile)
	st_size = st_results[6]
	if st_size > 5000:
	    st_size = st_size-5000

	self.file.seek(st_size)

	while True:
	    where = self.file.tell()
	    line  = self.file.readline()
	    process = False
	    if not line:
		time.sleep(0.1)
		self.file.seek(where)
	    else:
		suspectIP=""
		ip=()
		if "wrong password" in line.lower():
		    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )
		elif "rejected" in line.lower():
		    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )
		elif "no matching peer found" in line.lower():
		    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )

		if len(ip) > 1:
		    suspectIP = ip[1]
		elif len(ip) > 0:
		    suspectIP = ip[0]
		else:
		    suspectIP = ""

		return suspectIP


if __name__ == '__main__':
  try:
    sipcheck=SIPCheck()
  except KeyboardInterrupt:
	print "Exit"
	exit(1)
