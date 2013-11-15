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
import socket

class ShareList(object):
    ''' Share the ip address with distributed and descentralized servers '''

    host = 'www.google.com'
    port = 80

    def __init__(self,ip):
        self.logger = logging.getLogger('sipcheck')


    def connect(self):
        try:
            #create an AF_INET, STREAM socket (TCP)
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            self.logger.error('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
            sys.exit();
        try:
            remote_ip = socket.gethostbyname( self.host )

            # Esta linea devuelve una tupla con la lista de IPs que resuelven ese "host"
            # deberíamos probar todas ellas hasta que consigamos una con la que conectar.
            # remote_ip = socket.getaddrinfo(host, port, 0, 0, socket.SOL_TCP)
        except socket.gaierror:
            #could not resolve
            self.logger.error('Hostname could not be resolved. Exiting')
            sys.exit()
        self.logger.debug('Ip address of ' + self.host + ' is ' + remote_ip)
        #Connect to remote server
        self.s.connect((remote_ip , self.port))
        self.logger.info('Socket Connected to ' + self.host + ' on ip ' + remote_ip)


    def send_auth(self,sharedkey):
        self.logger.debug("Sending authentication: %s " % (sharedkey))
        self.send("SharedKey: %s" % (sharedkey))
        return True

    def send_ip(self,ip):
        self.send(ip)

    def send(self,string):
        message = string
        try :
            self.s.sendall(message+"\r\n\r\n")
        except socket.error:
            self.logger.error('Send failed: %s' % (message))
            sys.exit()
        self.logger.debug('Message send successfully')


    def report_ip(self,ip,sharedkey):
        self.logger.debug("Reporting attacker %s to sinologic.net" % (ip))
        try:
            self.logger.debug("Connecting to Sinologic Network")
            self.connect()
            if self.send_auth(sharedkey):
                self.send_ip(ip)
            else:
                self.logger.error("Invalid key")
        except Exception:
            self.logger.error("Unable connect to sinologic.net")



