#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
import socket

class distributedList:

    listaIP=[]

    def __init__(self,address,port,username,secret):
	try:
	    self.conectado=False
	    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    self.sock.settimeout(7)
	    self.sock.connect((address,port))
	    self.sock.settimeout(None)
	    self.sock.sendall('HELO\n')

	    data = self.sock.recv(1024)
	    data = data.replace('\r\n', '').strip()
	    if len(data.split(" ")) <= 1:
		print "Error"
	    else:
		codigos = data.split(" ")
		if len(codigos) < 2:
		    print "Error"
		else:
		    cod=codigos[1]
		    self.sock.sendall("USER %s %s" % (cod,username))
		    self.sock.sendall("PASS %s %s" % (cod,secret))
		    self.sock.settimeout(5)
		    data = self.sock.recv(1024)
		    data = data.replace('\r\n', '').strip()
		    self.sock.settimeout(None)
		    print "++"+data+"++"
		    if data.find("OK") >= 0:
			self.conectado=True
		    else:
			self.conectado=False
	except socket.error:
	    pass


    def get_ip_list(self):
	if self.conectado:
	    self.sock.sendall("GET UPDATED\n");
	    data = self.sock.recv(65000)
	    data = data.replace('\r\n', '').strip()
	    print "Recibido %s" % (data)