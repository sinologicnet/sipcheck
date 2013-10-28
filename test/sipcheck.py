#!/usr/bin/python -B
# -*- coding: utf-8 -*-

import configOptionsParser,iptablesController,sqlitedb,ignoreList
import time,sys,os,re


class SIPCheck(object):

    def __init__(self):

	# Inicialize sipcheck configuration file
	self.config=configOptionsParser.ConfigFile("sipcheck.conf")

	# Initialize iptables object with the ip list that we are going to ban
	# Parser iptables entries and insert into our local database
	self.iptables=iptablesController.IPTables()

	# Initialize database object to load ip list to ban
	self.db=sqlitedb.DB()

	# Inicialize list of host and networks to ignore
	self.ignoreList=ignoreList.IgnoreList("sipcheck.ignore")



    def run(self):
	# At self.iptables.listaIP we have all ip address banned (from sipcheck or other way)
	listaTBIP=self.iptables.listaIP

	# We get all entries blocked into our local database
	listaDBIP=self.db.ShowBlocked()

	# Each IP into database we must check if exists into iptables list
	for dbip in listaDBIP:
	    if dbip not in listaTBIP:
		self.iptables.banip(dbip)
		print "Añadida la IP",dbip,"en la tabla iptables"


	#Process Asterisk message file...
	print "Examinamos los mensajes de Asterisk..."
	while True:
	    ip=self.processFile()
	    if ip != "" and not self.ignoreList.isInList(ip) and ip not in self.iptables.listaIP:
		tries=self.db.InsertIP(ip)
		if tries > int(self.config.minticks):
		    print "Baneamos la IP",ip
		    self.db.BlockIP(ip)
		    self.iptables.banip(ip)



    def processFile(self):
	''' Method to read last lines of the message file and returns the attacker ip address '''
	self.file = open(self.config.messagefile, 'r')
	st_results = os.stat(self.config.messagefile)
	st_size = st_results[6]
	if st_size > self.config.messagebuffer:
	    st_size=st_size-self.config.messagebuffer

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

    def exit(self):
	# At self.iptables.listaIP we have all ip address banned (from sipcheck or other way)
	listaTBIP=self.iptables.listaIP

	# We get all entries blocked into our local database
	listaDBIP=self.db.ShowBlocked()

	# Each IP into database we must check if exists into iptables list
	for dbip in listaDBIP:
	    if dbip in listaTBIP:
		self.iptables.unbanip(dbip)
		print "Eliminada la IP",dbip,"de la tabla iptables"



if __name__ == '__main__':
    sipcheck=SIPCheck()
    try:
	sipcheck.run()
    except KeyboardInterrupt:
	sipcheck.exit()
	print "Exit"
	exit(1)
