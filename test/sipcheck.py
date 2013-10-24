#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configOptionsParser,iptablesController,sqlitedb
import time

def databaseUpdate():
  print "::databaseUpdate::"

def go():
    config=configOptionsParser.ConfigFile("sipcheck.conf")

    # Initialize iptables object with the ip list that we are going to ban
    iptables=iptablesController.IPTables()

#    iptables.banip("10.0.0.1")
#    iptables.show()
#    iptables.unbanip("10.0.0.1")
#    iptables.show()
    
    db=sqlitedb.DB()
    comandoSQL="INSERT INTO banned (ip) VALUES (\"90.90.90.90\");"
    print comandoSQL
    print db.sql(comandoSQL)
#    print db.sql("SELECT * FROM banned;")
    
    #db.sql("CREATE TABLE test1 (id INT PRIMARY KEY NOT NULL, ip VARCHAR(50))")

    # Check database to get the date of the last syncronization

    # If we aren't updated, we try connect to www.sinologic.net:6969 and ask for updated database that update to our local database

    # We need clear all our firewall from the ips of the local database to avoid repeat ip entries

    # Once updated, we open /var/log/asterisk/message file that comes from 'config['messagefile'] and read continuously looking for tryings and wrong passwords
    #messagefile=config['messagefile']
    #(messagefile)


if __name__ == '__main__':
  try:
	go()
  except KeyboardInterrupt:
	print "Exit"
	exit(1)
