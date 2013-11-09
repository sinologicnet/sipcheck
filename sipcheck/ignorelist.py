# -*- coding: utf-8 -*-

"""
functions was got from
http://stackoverflow.com/questions/819355/how-can-i-check-if-an-ip-is-in-a-network-in-python
Thanks to @saghul

Need to use IPv6 too
"""

import logging
import socket
import struct
import ipaddress

class IgnoreList(object):
    ''' Define if an IP is in ignore list '''

    def __init__(self, ignores):
        self.ignores = ignores
        self.logger = logging.getLogger('sipcheck')

    def s_check(self, ip_address):
        ''' check if IP is in ignore values '''
        ignored = False
        ip_address = struct.unpack('!L', socket.inet_aton(ip_address))[0]
        for net in self.ignores:
            if (ipaddress.ip_address(ip_address) in
                ipaddress.ip_network(unicode(net), strict=False)):
                ignored = True
        return ignored

    def dotted_quad_to_num(self, ip_address):
        ''' convert decimal dotted quad string to long integer '''
        return struct.unpack('!L', socket.inet_aton(ip_address))[0]
