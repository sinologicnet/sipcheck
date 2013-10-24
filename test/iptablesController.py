#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

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


    def banip(self,ip):
	''' Method to insert one IP address into the IPTables to ban some traffic comes from it. '''
	if ip not in self.listaIP:
	    comando=self.iptables+" -A INPUT -s "+ip+" -j DROP"
	    os.system(comando)
	    self.listaIP.append(ip)

    def unbanip(self,ip):
	''' Method to delete of the IPTables one IP address banned previously '''
	if ip in self.listaIP:
	    comando=self.iptables+" -D INPUT -s "+ip+" -j DROP"
	    os.system(comando);
	    self.listaIP.remove(ip)

    def unbanall(self):
	''' Method to delete all entries inserted for this module and get untouch old firewall tables '''
	for ip in self.listaIP:
	    comando=self.iptables+" -D INPUT -s "+ip+" -j DROP"
	    os.system(comando)
	    self.listaIP.remove(ip)

    def show(self):
	''' Show the IPTables '''
	comando=self.iptables+" -L"
	os.system(comando)

    def getList(self):
	return self.listaIP

