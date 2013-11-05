# -*- coding: UTF-8 -*-
"""
  Class for storing ips in SQLite3 database
"""

import sqlite3
import os.path

class DB(object):
    ''' Connection and operate with sqlite3 database '''
    dbfile = None

    def __init__(self, dbfile='sipcheck.db'):
        ''' Constructor of the class where we set where save db file '''
        self.dbfile = dbfile

    def check_db(self):
        '''  Verify file exists, is writable,
        is a valid sqlite3 file and contain all necessary tables '''

        status = True
        if os.path.isfile(self.dbfile) is not True:
            status = False
        return status

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
        except sqlite3.Error as error:
            print "Error in sql => %s" % error.args[0]
            #sys.exit(1)
        finally:
            if conn is not None:
                conn.close()
        return data

    def create_table(self):
        ''' Create de table escrutture '''
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
        ''' Return bloked IPS in banned table '''
        blocks = self.sql("SELECT ip FROM banned WHERE block = 1")
        response = []
        for block in blocks:
            response.append(block[0])
        return response

    def insert_ip(self, ipaddress, ntry=1):
        ''' Method to insert the IP into the table of banned ips '''
        existe = self.sql("SELECT try FROM banned WHERE ip = ?",
                        (ipaddress,))
        tries = 1
        if len(existe) is 0:
            existe = self.sql("INSERT INTO banned (ip) VALUES (?)",
                        (ipaddress, ))
        else:
            tries = int(existe[0][0]) + ntry
            existe = self.sql("""UPDATE banned SET
                updated_at=DATETIME('now'), try=? WHERE ip=?""",
                (tries, ipaddress, ))
        return tries

    def block_ip(self, ipaddress):
        ''' Block an IP address '''
        done = False
        self.insert_ip(ipaddress, 0)
        res = self.sql("""UPDATE banned
                        SET updated_at=DATETIME('now'), block = 1
                        WHERE ip=?""", (ipaddress, ))
        if res is not None:
            done = True
        return done

    def unblock_ip(self, ipaddress):
        ''' Unblock an IP address '''
        done = False
        self.insert_ip(ipaddress, 0)
        res = self.sql("""UPDATE banned
            SET updated_at=DATETIME('now'), block = 0 WHERE ip=?""",
            (ipaddress, ))
        if res is not None:
            done = True
        return done

    def delete_ip(self, ipaddress):
        ''' Delete an IP fron de table '''
        done = False
        self.insert_ip(ipaddress, 0)
        res = self.sql("DELETE FROM banned WHERE ip=?", (ipaddress, ))
        if res is not None:
            done = True
        return done

if __name__ == '__main__':
    ip_address = "192.168.1.2"
    sdb = DB('sipcheck.db')
    sdb.create_table()
    print sdb.show_blocked()
    print "Intentos: %r" % sdb.insert_ip(ip_address)
    print sdb.show_ips()
    print sdb.block_ip(ip_address)
    print sdb.unblock_ip(ip_address)
    print sdb.block_ip("192.168.1.3")
    print sdb.delete_ip("192.168.1.3")
