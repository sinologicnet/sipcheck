#!/usr/bin/env python -B
# -*- coding: UTF-8 -*-

import sqlite3 as lite
import sys,os
import time

class DB:

    def __init__(self):
	''' Constructor of the class '''
	self.dbfile = 'sipcheck.db'


    def sql(self,sql):
	''' Method to connect and execute some SQL sentence '''
	con = None
	data= None
	try: 
	    con = lite.connect(self.dbfile)
	    cur = con.cursor()
	    cur.execute(sql)
	    con.commit()
	    data = cur.fetchall()
	except lite.Error, e:
	    print "Error %s:" % e.args[0]
	    sys.exit(1)

	finally:
	    if con:
		con.close()
	return data


    def showTables(self):
	''' Method to show all tables of the database '''
	print self.sql("SELECT name FROM sqlite_master WHERE type = 'table'")



    def showTable(self,table):
	print self.sql("PRAGMA table_info("+str(table)+")")



    def ShowIP(self):
	print self.sql("SELECT * FROM banned")




    def InsertIP(self,ip):
	''' Method to insert the IP into the table of banned ips '''
	existe=self.sql("SELECT * FROM banned WHERE ip='"+ip+"'")
	now=time.strftime('%Y-%m-%d %H:%M:%S')
	tries=1;
	if len(existe) == 0:
	    existe=self.sql("INSERT INTO banned (ip,date,try,block) VALUES ('"+ip+"','"+str(now)+"',"+str(tries)+",0)")
	else:
	    tries=int(existe[0][3])+1
	    blocks=int(existe[0][4])
	    existe=self.sql("UPDATE banned SET date='"+str(now)+"', try="+str(tries)+", block="+str(blocks)+" WHERE ip='"+ip+"'")
	return tries

    def BlockIP(self,ip):
	''' Method to insert the IP into the table of banned ips '''
	existe=self.sql("SELECT * FROM banned WHERE ip='"+ip+"'")
	now=time.strftime('%Y-%m-%d %H:%M:%S')
	tries=1;
	if len(existe) == 0:
	    existe=self.sql("INSERT INTO banned (ip,date,try,block) VALUES ('"+ip+"','"+str(now)+"',"+str(tries)+",1)")
	else:
	    tries=int(existe[0][3])+1
	    blocks=int(existe[0][4])+1
	    existe=self.sql("UPDATE banned SET date='"+str(now)+"', try="+str(tries)+", block="+str(blocks)+" WHERE ip='"+ip+"'")
	return tries



    def DeleteIP(self,ip):
	''' Method to delete the record of one banned ip '''
	existe=self.sql("SELECT * FROM banned WHERE ip='"+ip+"'")
	if len(existe) >= 0:
	    existe=self.sql("DELETE banned WHERE '"+ip+"'")

