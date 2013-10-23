#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from subprocess import call,check_output

class Iptables(object):

  def addIPBanned(self,IP):
	print "Añadiendo IP",IP,"a la lista de baneados"
	self.listaIP.append(IP)
	self.listaIP = list(set(self.listaIP))


  def remIPBanned(self,IP):
	print "Eliminando la IP",IP,"a la lista de baneados"
	


  def clearTable(self):
	print "Limpiando tabla de IPTables"
	for ipban in self.listaIP:
	  print "Eliminando",ipban,"de la tabla del firewall"
	  comando="iptables -D INPUT -s "+ipban+" -j DROP"
	  try: 
		print check_output(comando, shell=True)
	  except:
		pass


  def commit(self):
	print "Aplicando",len(self.listaIP),"cambios al firewall"
	self.clearTable()
	for ipban in self.listaIP:
	  comando="iptables -A INPUT -s "+ipban+" -j DROP"
	  print comando
	  print check_output(comando, shell=True)

	  comando="iptables -L"
	  print check_output(comando, shell=True)


  def __init__(self):
	print "Iniciando objeto IPTables"
	self.listaIP=[]
