#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import socket,struct

class IgnoreList:

    def __init__(self,archivo):
	''' Constructor of the class '''
	self.data = [line.strip() for line in open(archivo, 'r')]


    def isInList(self,ip):
	try:
	    nip=self.dottedQuadToNum(ip)
	    estaEnLaLista=False
	    for red in self.data:
		nnet=red.split("/")
		netw=nnet[0]
		mask=nnet[1]
		netmask=self.networkMask(str(netw),int(mask))
		if self.addressInNetwork(nip,netmask):
		    estaEnLaLista=True
		    print "Dirección IP",ip,"está en la lista blanca"
	except:
	    estaEnLaLista=False
	return estaEnLaLista

    """
	Next functions was got from 
	http://stackoverflow.com/questions/819355/how-can-i-check-if-an-ip-is-in-a-network-in-python
	Thanks to @saghul 
    """

    def makeMask(self,n):
	"return a mask of n bits as a long integer"
	return (2L<<n-1) - 1

    def dottedQuadToNum(self,ip):
	"convert decimal dotted quad string to long integer"
	return struct.unpack('!L',socket.inet_aton(ip))[0]

    def networkMask(self,ip,bits):
	"Convert a network address to a long integer" 
	return self.dottedQuadToNum(ip) & self.makeMask(bits)

    def addressInNetwork(self,ip,net):
	"Is an address in a network"
	return ip & net == net

