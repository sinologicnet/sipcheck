#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

"""
    Clase que permite gestionar unas acciones básicas del firewall mediante IPTables
"""


class IPTables(object):

    iptables="/sbin/iptables"
    listaIP=[]

    def __init__(self):
	''' constructor que no hace nada '''


    def banip(self,ip):
	''' Método para insertar una ip en la tabla IPTables para rechazar cualquier tráfico proveniente de ella '''
	if ip not in self.listaIP:
	    comando=self.iptables+" -A INPUT -s "+ip+" -j DROP"
	    os.system(comando)
	    self.listaIP.append(ip)

    def unbanip(self,ip):
	''' Método para eliminar de la tabla de IPTables una IP baneada previamente '''
	if ip in self.listaIP:
	    comando=self.iptables+" -D INPUT -s "+ip+" -j DROP"
	    os.system(comando);
	    self.listaIP.remove(ip)

    def show(self):
	''' Rechazar cualquier tráfico procedente de la direccion IP determinada '''
	comando=self.iptables+" -L"
	os.system(comando)

    def getList(self):
	return self.listaIP

