#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configOptionsParser,iptablesController
import time

def databaseUpdate():
  print "::databaseUpdate::"

def go():
  # Shall we run in background process?

  # We read the configuration of the user from ./sipcheck.conf or /etc/sipcheck.conf if first one doesn't exists.
  config=configOptionsParser.ConfigFile("sipcheck.conf")

  # Initialize iptables object with the ip list that we are going to ban
  iptables=iptablesController.Iptables()

  # Check database to get the date of the last syncronization

  # If we aren't updated, we try connect to www.sinologic.net:6969 and ask for updated database that update to our local database

  # We need clear all our firewall from the ips of the local database to avoid repeat ip entries
  iptables.addIPBanned("10.0.0.1");
  iptables.commit()

  # Once updated, we open /var/log/asterisk/message file that comes from 'config['messagefile'] and read continuously looking for tryings and wrong passwords
  #messagefile=config['messagefile']
  #(messagefile)


if __name__ == '__main__':
  try:
	go()
  except KeyboardInterrupt:
	print "Exit"
	exit(1)
