#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    SIPCheck is a tool that parse the file /var/log/asterisk/messages looking for error and 
    warnings messages from unauthorized access or trying calls from anonymous users and add 
    their ip to the firewall and warns to sinologic server to add for global list of banned 
    ip.
'''

'''
    Check if our database is available and get when was the last time we run this script

    Database has got this tables:
	- ipbanned : table with the list of the ip banned on Sinologic.
	- configure: table with the values of:
		+ last time we run this script
		+ datetime of the ipbanned table
		+ 
	- ipsuspect: table with the list of the ip suspected of attacks
	

    1. Get all values of the "configure" table.
    2. Check the datetime of the ipbanned table:
    2.1. If datetime is > 48 h, connect to Sinologic and download the new list of ip banned.
    3. Check /var/log/asterisk/messages and looking for 'Wrong password' or 'rejected' words
    3.1. For each line found, we parser the line and get the IP address suspected (IPAS).
    3.2. If IPAS exists in ipsuspect table, do nothing. Else, insert into the ipsuspect table.
    4. Once the parser has finished to analyze the log file, create a request to send like POST method all ipsuspect found.
    5. If it is required, add to the firewall new ip address suspected.

'''

import time, os, re
import threading

from incl.sqlitedb import DB
from incl.block import IPT

############################################
#  Conf:
logfile = 'log.txt'

############################################

class GetAttackers(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        #Creating object that manages database
        db = DB()

        #Open file to read
        file = open(logfile, 'r')

        #Find the size of the file and move to the end
        st_results = os.stat(logfile)
        st_size = st_results[6]
        file.seek(st_size)

        while 1:
            where = file.tell()
            line  = file.readline()

            if not line:
                time.sleep(0.2)
                file.seek(where)
            else:
                #If line contents "markers" get IP
                if "Wrong password" in line:
                    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )
                    #Add ip to db
                    db.InsertIP(ip[0])

                if "rejected" in line:
                    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )
                    #Add ip to db
                    db.InsertIP(ip[0])


class BlockAttackers(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        #Creating object that manages database
        db = DB()
        #Creating object that blocks ofender
        block = IPT()

        while 1:
            #Get all IPs with max trys and block them
            for ip in db.GetIPsToBlock():
                print "Blocking IP: " + ip[0]
                block.BlockIP(ip[0])
           
            time.sleep(1)




def go():
        getattackers   = GetAttackers()
        blockattackers = BlockAttackers()

        getattackers.start()
        blockattackers.start()

        getattackers.join()
        blockattackers.join()


if __name__ == '__main__':
   try:
      go()
   except KeyboardInterrupt:
      # do nothing here
      pass

