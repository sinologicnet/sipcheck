#!/usr/bin/python -B
# -*- coding: utf-8 -*-

""" sipcheck.py: Core of the sipcheck application."""

__author__ = "Elio Rojano, Sergio Cotelo, Javier Vidal"
__copyright__ = "Copyright 2013, Sinologic.net"
__credits__ = ["Saúl Ibarra"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Elio Rojano"
__date__ = "2013-10-25"
__email__ = "sipcheck@sinologic.net"
__status__ = "Production"


import configOptionsParser,iptablesController,sqlitedb,ignoreList,distributedList
import time,sys,os,re


class SIPCheck(object):

    def __init__(self):
	print "Starting SIPCheck "+__version__+"..."
	# Inicialize sipcheck configuration file
	self.config=configOptionsParser.ConfigFile("sipcheck.conf")

	# Initialize iptables object with the ip list that we are going to ban
	# Parses iptables entries and insert into our local database
	self.iptables=iptablesController.IPTables()

	# Initialize database object to load ip list to ban
	self.db=sqlitedb.DB()

	# Inicialize list of host and networks to ignore
	self.ignoreList=ignoreList.IgnoreList("sipcheck.ignore")

	if self.config.shared:
	    self.distributedList=distributedList.distributedList("sipcheck.sinologic.net",6969,self.config.username,self.config.password)
	    if self.distributedList.conectado:
		print self.distributedList.get_ip_list()

    def run(self):

	# At self.iptables.listaIP we have all ip address banned (from sipcheck or other way)
	listaTBIP=self.iptables.listaIP

	# We get all entries blocked into our local database
	listaDBIP=self.db.show_blocked()

	# Each IP into database we must check if exists into iptables list
	for dbip in listaDBIP:
	    if dbip not in listaTBIP:
		self.iptables.banip(dbip)


	#Process Asterisk message file...
	while True:
	    ip=self.processFile()
	    if ip != "" and not self.ignoreList.isInList(ip) and ip not in self.iptables.listaIP:
		tries=self.db.insert_ip(ip)
		if tries > int(self.config.minticks):
		    self.db.block_ip(ip)
		    self.iptables.banip(ip)



    def processFile(self):
	''' Method to read last lines of the message file and returns the attacker ip address '''
	self.file = open(self.config.messagefile, 'r')
	st_results = os.stat(self.config.messagefile)
	st_size = st_results[6]
	if st_size > self.config.messagebuffer:
	    st_size=st_size-self.config.messagebuffer

	self.file.seek(st_size)
	print "Waiting for attackers..."
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
	listaDBIP=self.db.show_blocked()

	# Each IP into database we must check if exists into iptables list
	for dbip in listaDBIP:
	    if dbip in listaTBIP:
		self.iptables.unbanip(dbip)



if __name__ == '__main__':
    sipcheck=SIPCheck()
    try:
	sipcheck.run()
    except KeyboardInterrupt:
	sipcheck.exit()
	print "Exit"
	exit(1)
