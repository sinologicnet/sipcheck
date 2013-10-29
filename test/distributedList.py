#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class distributedList:

    listaIP=[]

    def __init__(self,username,secret):
	print "Conectamos con Sinologic"
	print "Nos autentificamos con username",username,"y secret",secret
	print "Pedimos la lista de ips globales a banear"
	print "las recogemos y la guardamos en la listaIP"
	listaIP.append("10.10.10.10");
	listaIP.append("20.20.20.20");
	print "
