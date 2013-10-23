#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3 as lite
import sys,os
import time

class DB:

    def __init__(self):
	self.dbfile = 'sipcheck.db'
	
	'''
	    Table: banned
	    Fields:
		id INTEGER PRIMARY KEY AUTOINCREMENT
		ip CHAR(50)
		try INTEGER
		date DATETIME
		block INTEGER
	'''
	

    def sql(self,sql):
	con = None
	data= None
	try: 
	    con = lite.connect(self.dbfile)
	    cur = con.cursor()
	    cur.execute(sql)
	    data = cur.fetchall()
	except lite.Error, e:
	    print "Error %s:" % e.args[0]
	    sys.exit(1)

	finally:
	    if con:
		con.close()
	return data




    def showTables(self):
	''' Método para mostrar todas las tablas de la base de datos '''
	print self.sql("SELECT name FROM sqlite_master WHERE type = 'table'")



    def showTable(self,table):
	print self.sql("PRAGMA table_info("+str(table)+")")

