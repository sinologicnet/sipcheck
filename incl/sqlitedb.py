#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3 as lite
import sys
import time

class DB:

    dbfile = 'database.db'

    def InsertIP(self, ip):
        
        con = None

        try:
            con = lite.connect(self.dbfile)

            cur = con.cursor()
            cur.execute("SELECT * FROM IPAS WHERE ip = '"+ip+"'")

            data = cur.fetchone()

            now = time.time()
            if data:
                #update
                cur.execute("UPDATE IPAS SET try = '"+ str(int(data[2])+1) +"', date = '"+str(now)+"' WHERE ip = '"+ip+"'")
                con.commit()
                print "existe"

            else:
                #insert
                cur.execute("INSERT INTO IPAS (ip,try,date) VALUES ('"+ip+"',1,'"+str(now)+"')")
                con.commit()
                print "non existe"

        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:
            if con:
                con.close()

    def GetTrys(self, ip):
	
	con = None	

	try:
	    con = lite.connect(self.dbfile)
	    
	    cur = con.cursor()
	    cur.execute("SELECT try from IPAS where ip = '"+ip+"'")

	    data = cur.fetchone()
	    print "Intentos: " + str(data[0])

        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:
            if con:
                con.close()

    def CleanIP(self, ip):

        con = None

        try:
            con = lite.connect(self.dbfile)

            cur = con.cursor()
            cur.execute("DELETE from IPAS where ip = '"+ip+"'")
            con.commit()

        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:
            if con:
                con.close()

