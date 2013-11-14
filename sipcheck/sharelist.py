# -*- coding: utf-8 -*-

"""
Need to use IPv6 too
"""

import logging
import socket

class ShareList(object):
    ''' Share the ip address with distributed and descentralized servers '''

    def __init__(self):
        self.logger = logging.getLogger('sipcheck')


    def connect(self):
        self.logger.debug("Connecting to Sinologic Network")
