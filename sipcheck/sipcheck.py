# -*- coding: utf-8 -*-
'''
    Program
'''

import logging
import sys
import re
import os
import time
from threading import Thread

from .config import Config
from .db import DB
from .ignorelist import IgnoreList
from .iptables import IPTables
from .sharelist import ShareList

class SIPCheck(Thread):
    ''' Main class '''
    levels = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}

    def __init__(self, config_file):
        Thread.__init__(self)
        self.work = True
        self.logger = logging.getLogger('sipcheck')
        self.config = Config(config_file)
        self.setup_logger(self.config.get_general('logfile'),
            self.config.get_general('loglevel'))

        self.ip_dbs = self.init_db(self.config.get_database('file'))
        if self.ip_dbs is None:
            sys.exit(-1)

        self.ignore_list = self.load_ignored()

        useiptables = self.config.get_general('useiptables')
        if useiptables:
            self.useiptables=useiptables
            self.logger.info("Will block IPs with iptables")
            self.ipt = IPTables()

        useshared = self.config.get_shared('enable')
        if useshared:
            self.useshared=useshared
            self.logger.info("Will report attackers from/to external server")
            self.sharedkey = self.config.get_shared('key')
            self.logger.debug("Read useshared as '%s'",useshared)



    def run(self):
        stimes = 0

        ''' If we allow remote service, we connect and download all known ip attackers '''
        if self.useshared:
            self.share = ShareList(self.sharedkey)
            listOfIPS=self.share.getAll()
            self.logger.debug("Recibida lista: ");
            for remoteIP in listOfIPS:
                if not self.ignore_list.s_check(remoteIP):
                    if not self.ip_dbs.check_bannedip(remoteIP):
                        self.logger.debug("Added %s into database" % remoteIP)
                        self.ip_dbs.block_ip(remoteIP)

                    if self.useiptables:
                        self.ipt.unblock(remoteIP)
                        self.ipt.block(remoteIP)
                        self.logger.debug("IP Address %s already marked as banned. Ignored" % remoteIP);

        asterisk_log = self.load_logfile()

        while self.work:
            where = asterisk_log.tell()
            line  = asterisk_log.readline()

            if not line:
                if stimes is 5:
                    asterisk_log = self.load_logfile()

                time.sleep(1)
                asterisk_log.seek(where)
                stimes += 1
            else:
                stimes = 0
                if self.is_attack(line):
                    numips=len(re.findall( r'[0-9]+(?:\.[0-9]+){3}', line ))
                    ipaddress = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )[numips-1]
                    if self.ignore_list.s_check(ipaddress):
                        self.logger.info("IP %s on ignore" % ipaddress)
                    else:
                        tries = self.add_ip(ipaddress)
                        if tries >= int(self.config.get_general('minticks')):
                            self.logger.debug("Suspicious IP has become an attacker: %s" % ipaddress)
                            self.ip_dbs.block_ip(ipaddress)
                            if self.useiptables:
                                self.ipt.unblock(ipaddress)
                                self.ipt.block(ipaddress)
                                self.logger.debug("IPT block: %s" % ipaddress)
                            if self.useshared:
                                self.share.report(ipaddress)

    def quit(self):
        ''' stop Thread '''
        self.logger.debug("Stop requested")
        self.work = False

    def load_logfile(self):
        ''' Load the log file to read '''
        self.logger.debug("Reading logs from %s" %
            self.config.get_general('messagefile'))

        asterisk_log = open(self.config.get_general('messagefile'), 'r')

        #Find the size of the file and move to the end
        st_results = os.stat(self.config.get_general('messagefile'))
        st_size = st_results[6]
        asterisk_log.seek(st_size)
        return asterisk_log

    def load_ignored(self):
        ''' Load ignored ips '''
        self.logger.debug("IPS on ignore : %r" % self.config.get_ignore())
        return IgnoreList(self.config.get_ignore())

    def setup_logger(self, logfile, loglevel):
        ''' Enable logger settings '''
        logformat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.logger.info("Internal logs will be stored at %s file." % logfile)

        # create a file handler
        handler = logging.FileHandler(logfile)
        handler.setLevel(level=self.levels[loglevel])

        # create a logging format
        formatter = logging.Formatter(logformat)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        logging.basicConfig(level=self.levels[loglevel])

    def init_db(self, dbfile):
        ''' Init database '''
        self.logger.debug("Using %s file as database" % dbfile)
        bdb = DB(dbfile)
        if bdb.exists() is not True:
            self.logger.debug("DataBase doesn't exist, creating...")
            bdb.create_table()

        if bdb.check() is not True:
            self.logger.error("ERROR: Can't create database file.")
            return None
        return bdb

    def is_attack(self, line):
        ''' Parse line string '''
        if "rejected" in line:
            return True
        if "Wrong password" in line:
            return True
        if "failed to authenticate" in line:
            return True
        return False

    def add_ip(self, ipaddress):
        ''' Add IP to database '''
        return self.ip_dbs.insert_ip(ipaddress)
