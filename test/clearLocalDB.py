#!/usr/bin/python -B
# -*- coding: utf-8 -*-

import configOptionsParser,iptablesController,sqlitedb
import time,sys,os,re

def databaseUpdate():
  print "::databaseUpdate::"

def go():
    config=configOptionsParser.ConfigFile("sipcheck.conf")
    iptables=iptablesController.IPTables()
    db=sqlitedb.DB()
    now=time.time()

    confirm="?"
    while confirm.lower() != "y" and confirm.lower() != "n":
	confirm=raw_input("Are you sure that you want clean all ip banned from your local database? [y|n]")
	print "All ip banned into local database are cleaned"
	db.sql("DELETE FROM banned")
    



if __name__ == '__main__':
  try:
	go()
  except KeyboardInterrupt:
	print "Exit"
	exit(1)
