# -*- coding: utf-8 -*-

"""
Objetivo de este módulo
    - Obtener la lista de todos los "hosts" que resuelven el nombre. sipcheck.sinologic.net
    - Establecer la conexión (estableciendo un timeout de conexión) con alguna de las máquinas obtenidas.
    - Enviar la 'key' que identifica al usuario en el sistema y autentificarlo.
    - Una vez autentificado, enviar la dirección IP atacante.
    - Finalmente, desconectar del servicio para no ocupar un socket nuevo y ahorrar ancho de banda.
"""

import logging
import urllib2
import socket
import json
import random

# para long2ip
from socket import inet_ntoa
from struct import pack


class ShareList(object):
    ''' Share the ip address with distributed and descentralized servers '''

    host = 'sipcheck.sinologic.net'
    timeout = 10
    key = ''

    ''' Al ejecutar el sistema, enviamos la versión de actualización que tenemos
        en nuestra base de datos interna y el servidor nos devuelve la lista de
        todas las ips oficiales y mis candidatas.
    '''
    def __init__(self,key):
        self.logger = logging.getLogger('sipcheck')
        self.key=key
        self.logger.debug("Using the unique key: %s" % self.key)
    

    def getAll(self):
        socket.setdefaulttimeout(self.timeout)
        html=""
        listaCompleta=[]
        try:
            response = urllib2.urlopen("http://%s/candidates/getAll/%s/" % (self.host,self.key))
            html = response.read().strip()
            listaCompleta=html.split(",")
        except Exception:
            self.logger.error("Server %s not found" % (self.host))
        return listaCompleta

    def get(self, version=0):
        ''' If we send version=0 we will receive only the ip address to ban, else we will receive the changes from version value '''
        socket.setdefaulttimeout(self.timeout)
        cambios=[]
        try:
            response = urllib2.urlopen("http://%s/get/%s/%s" % (self.host,self.key,version))
            html = response.read().strip()
            cambios=json.loads(html)
            numcambios=len(cambios)
        except Exception:
            self.logger.error("Server %s not found" % (self.host))
        return cambios


    def report(self,ip):
        socket.setdefaulttimeout(self.timeout)
        html=""
        listaCompleta=[]
        try:
            response = urllib2.urlopen("http://%s/candidates/put/%s/%s" % (self.host,self.key,ip))
            html = response.read().strip()
            listaCompleta=html.split(",")
        except Exception:
            self.logger.error("Server %s not found" % (self.host))
        return listaCompleta


        ''' Once detected the attacker ip, we report it to sipcheck.sinologic.net '''
        self.logger.info("Hi %s, we are under attack from %s" % (self.key,ip))
        
