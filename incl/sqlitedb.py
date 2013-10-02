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
        print "Intentos por IP"

    def CleanIP(self, ip):
        print "Limpiando bbdd"



