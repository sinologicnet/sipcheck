# -*- coding: utf-8 -*-
'''
    Wrapper for use iptables and block IPs
'''
import logging
import os

class IPTables(object):
    ''' IPTables wrapper '''
    dbconn = None

    def __init__(self):
        ''' Constructor '''
        self.logger = logging.getLogger('sipcheck')

    def block(self, ipaddress):
        ''' Set an IP adress as blocked and block with iptables '''
        self.logger.debug('Blocking %s IP address' % ipaddress)
        os.system ("iptables -A INPUT -s %s -j DROP" % ipaddress)
        return True

    def unblock(self, ipaddress):
        ''' Unset an IP as bloked and release iptables block '''
        self.logger.debug('Unblocking %s IP address' % ipaddress)
        os.system ("iptables -D INPUT -s %s -j DROP" % ipaddress)
        return True

