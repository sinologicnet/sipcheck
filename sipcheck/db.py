# -*- coding: UTF-8 -*-
"""
  Class for storing ips in SQLite3 database
"""

import logging
import sqlite3
import os.path

class DB(object):
    ''' Connection and operate with sqlite3 database '''
    dbfile = None

    def __init__(self, dbfile='sipcheck.db'):
        ''' Constructor of the class where we set where to save db file '''
        self.dbfile = dbfile
        self.logger = logging.getLogger('sipcheck')
        self.logger.debug("DataBase object created")

    def exists(self):
        '''  Verify if file exists '''
        return os.path.isfile(self.dbfile)

    def check(self):
        '''  Is writable, is a valid sqlite3 file and contains all necessary tables '''
        if self.exists() is not True:
            self.logger.debug("DataBase doesn't exist")
            return False
        if os.access(self.dbfile, os.R_OK) is not True:
            self.logger.debug("DataBase isn't readable")
            return False
        if os.access(self.dbfile, os.W_OK) is not True:
            self.logger.debug("DataBase isn't writable")
            return False
        return True

    def sql(self, sql, params=()):
        ''' Method to connect and execute some SQL sentence '''
        conn = None
        data = None
        try:
            conn = sqlite3.connect(self.dbfile)
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            data = cur.fetchall()
        except sqlite3.Error:
            data = None
            #print "Error in sql => %s" % error.args[0]
            #sys.exit(1)
        finally:
            if conn is not None:
                conn.close()
        return data

    def create_table(self):
        ''' Creation of table structure '''
        self.logger.debug("Creating table")
        return self.sql("""CREATE TABLE banned
                        (ip,
                        try DEFAULT 0,
                        block DEFAULT 0,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                        )""")

    def show_ips(self):
        ''' Return IPS in banned table '''
        return self.sql("""SELECT ip, try, block, created_at, updated_at 
	    FROM banned""")

    def show_blocked(self):
        ''' Return IP blocked from banned table '''
        blocks = self.sql("SELECT ip FROM banned WHERE block = 1")
        response = []
        for block in blocks:
            response.append(block[0])
        return response

    def check_bannedip(self, ipaddress):
        ''' Method to check if ip is into the table of banned ips '''
        self.logger.debug("Checking if %s is into the table" % ipaddress)
        existe = self.sql("SELECT try FROM banned WHERE ip = ?", (ipaddress,))
        return len(existe) > 0

    def insert_ip(self, ipaddress, ntry=1):
        ''' Method to insert IP into the table of banned ips '''
        self.logger.debug("Inserting IP %s" % ipaddress)
#        existe = self.sql("SELECT try FROM banned WHERE ip = ?",
#                        (ipaddress,))

        tries = 1
        if not self.check_bannedip(ipaddress):
#        if len(existe) is 0:
            existe = self.sql("INSERT INTO banned (ip) VALUES (?)",
                        (ipaddress, ))
        else:
            tries = int(existe[0][0]) + ntry
            existe = self.sql("""UPDATE banned SET
                updated_at=DATETIME('now'), try=? WHERE ip=?""",
                (tries, ipaddress, ))
        return tries

    def block_ip(self, ipaddress):
        ''' Block IP address '''
        self.logger.debug("Block IP %s" % ipaddress)
        done = False
        self.insert_ip(ipaddress, 0)
        res = self.sql("""UPDATE banned
                        SET updated_at=DATETIME('now'), block = 1
                        WHERE ip=?""", (ipaddress, ))
        if res is not None:
            done = True
        return done

    def unblock_ip(self, ipaddress):
        ''' Unblock IP address '''
        self.logger.debug("Unblock IP %s" % ipaddress)
        done = False
        self.insert_ip(ipaddress, 0)
        res = self.sql("""UPDATE banned
            SET updated_at=DATETIME('now'), block = 0 WHERE ip=?""",
            (ipaddress, ))
        if res is not None:
            done = True
        return done

    def delete_ip(self, ipaddress):
        ''' Delete IP from the table '''
        self.logger.debug("Delete IP %s" % ipaddress)
        done = False
        self.insert_ip(ipaddress, 0)
        res = self.sql("DELETE FROM banned WHERE ip=?", (ipaddress, ))
        if res is not None:
            done = True
        return done
