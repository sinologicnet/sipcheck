# -*- coding: utf-8 -*-

"""
functions was got from
http://stackoverflow.com/questions/819355/how-can-i-check-if-an-ip-is-in-a-network-in-python
Thanks to @saghul

Need to use IPv6 too
"""

import socket
import struct

class IgnoreList(object):
    ''' Define if an IP is in ignore list '''

    def __init__(self, ignores):
        self.ignores = ignores

    def is_ignored(self, ipaddress):
        ''' check if IP is in ignore values '''
        ignored = False
        try:
            current_ip = self.dotted_quad_to_num(ipaddress)
            for net in self.ignores:
                net_parts = net.split("/")
                network = net_parts[0]
                mask = net_parts[1]
                netmask = self.network_mask(str(network), int(mask))
                if self.address_in_network(current_ip, netmask):
                    ignored = True
        except Exception as excep:
            ignored = False

        return ignored

    def make_mask(self, net_bits):
        ''' return a mask of n bits as a long integer '''
        return (2L<<net_bits-1) - 1

    def dotted_quad_to_num(self, ipaddress):
        ''' convert decimal dotted quad string to long integer '''
        return struct.unpack('!L', socket.inet_aton(ipaddress))[0]

    def network_mask(self, ipaddress, bits):
        ''' Convert a network address to a long integer '''
        return self.dotted_quad_to_num(ipaddress) and self.make_mask(bits)

    def address_in_network(self, ipaddress, net):
        ''' Is an address in a network '''
        return ipaddress & net == net
