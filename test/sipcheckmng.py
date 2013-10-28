#!/usr/bin/python -B
# -*- coding: utf-8 -*-

"""
    This application is used to delete all entries of local database of ip banned
"""


import configOptionsParser,iptablesController,sqlitedb
import time,sys,os,re

def databaseUpdate():
  print "::databaseUpdate::"

def go():
    config=configOptionsParser.ConfigFile("sipcheck.conf")
    iptables=iptablesController.IPTables()
    db=sqlitedb.DB()
    now=time.time()

    option="?"
    while option.lower() != "q":
	print "SIPCHECK MENU OPTIONS"
	print "--------------------------------------------------"
	print " a) Clean all ip banned from local database "
	print " b) Show all ip banned"
	print " c) Remove IP address from table"
	print ""
	print " q) Quit"
	print "--------------------------------------------------"
	option=raw_input("Your choose:")

	if option.lower() == "a":
	    confirm=raw_input("Are you sure that you want clean all ip banned from your local database? ")
	    if confirm.lower() == "y" or confirm.lower() == "s":
		print "All ip banned into local database are cleaned"
		db.sql("DELETE FROM banned")

	elif option.lower() == "b":
	    lista=db.sql("SELECT * FROM banned WHERE block != 0")
	    if len(lista) == 0:
		print "There aren't ip address on the list"
	    else:
		for t in lista:
		    print "    IP    \t    DATE    \t      TRY \t BLOCKED"
		    print str(t[1]),"\t",str(t[2]),"\t",str(t[3]),"\t",str(t[4])

	elif option.lower() == "c":
	    confirm=raw_input("Enter the IP address to remove of your ban list:")
	    if db.DeleteIP(confirm):
		print "IP address",confirm,"has been deleted of the local database"
	    else:
		print "IP address",confirm,"not found in local database"

	print ""



if __name__ == '__main__':
  try:
	os.system("clear")
	go()
  except KeyboardInterrupt:
	print "Exit"
	exit(1)
