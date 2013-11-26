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

class ShareList(object):
    ''' Share the ip address with distributed and descentralized servers '''

    host = 'sipcheck.sinologic.net'
    timeout = 5
    key = ''

    def __init__(self,key):
        self.logger = logging.getLogger('sipcheck')
        self.key=key
        self.logger.debug("Using the unique key: %s" % self.key)
        socket.setdefaulttimeout(self.timeout)
        response = urllib2.urlopen('http://%s/now' % self.host)
        html = response.read().strip()
        self.logger.debug(html)

    def get(self, version=0):
        ''' If we send version=0 we will receive only the ip address to ban, else we will receive the changes from version value '''
        socket.setdefaulttimeout(self.timeout)
        response = urllib2.urlopen("http://%s/get?key=%s&version=%s" % (self.host,self.key,version))
        html = response.read().strip()
        cambios=json.loads(html)
        numcambios=len(cambios)
        return cambios


    def report(self,ip):
        ''' Once detected the attacker ip, we report it to sipcheck.sinologic.net '''
        self.logger.info("Hi %s, we are under attack from %s" % (self.key,ip))
        