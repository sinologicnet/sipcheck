#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os,re

"""
    Clase que permite gestionar unas acciones básicas del firewall mediante IPTables
    El comportamiento es bien sencillo, únicamente sirve para bloquear IP, desbloquear IPs
    y mostrar la tabla actual.
    Paralelamente lleva una lista con las direcciones IP bloqueadas para evitar bloquear doblemente
    algunas direcciones que ya han sido bloquadas (iptables permite banear N veces a una IP)
"""


class IPTables(object):

    iptables="/sbin/iptables"
    listaIP=[]

    def __init__(self):
	''' constructor que no hace nada '''

	# Vamos a consultar qué direcciones IP tenemos en el firewall
	proc = subprocess.Popen(['iptables', '-L', '-n'],stdout=subprocess.PIPE)
	for line in proc.stdout:
	    line = line.strip()
	    if "DROP" in line.split("\n"):
		ips=re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)
		ip=ips[0]
		# Metemos las entradas del firewall en la lista
		self.listaIP.append(ip)

    def banip(self,ip):
	''' Method to insert one IP address into the IPTables to ban some traffic comes from it. '''
	comando=self.iptables+" -A INPUT -s "+ip+" -j DROP"
	os.system(comando)
	self.listaIP.append(ip)

    def unbanip(self,ip):
	''' Method to delete of the IPTables one IP address banned previously '''
	comando=self.iptables+" -D INPUT -s "+ip+" -j DROP"
	os.system(comando);
	if ip in self.listaIP:
	    self.listaIP.remove(ip)

    def unbanall(self):
	''' Method to delete all entries inserted for this module and get untouch old firewall tables '''
	for ip in self.listaIP:
	    comando=self.iptables+" -D INPUT -s "+ip+" -j DROP"
	    os.system(comando)
	    if ip in self.listaIP:
		self.listaIP.remove(ip)

    def show(self):
	''' Show the IPTables '''
	comando=self.iptables+" -L -n"
	os.system(comando)

    def getList(self):
	return self.listaIP

