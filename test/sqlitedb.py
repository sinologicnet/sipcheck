# -*- coding: UTF-8 -*-

import sqlite3 as lite
import os

class DB(object):

	dbfile = None
	conn = None

	def __init__(self, file='sipcheck.db'):
		''' Constructor of the class '''
		self.dbfile = file
		if not self.check():
		    self.create_table()

	def check(self):
		''' TODO: Verify file exists, is writable, is a valid sqlite3 file
		and contain all necessary tables  '''
		status=False
		try:
		    with open(self.dbfile):
			status=True
		except IOError:
		    print 'Warning! %s not found. We must to create it.' % (self.dbfile)
		    # Check if this path is writable
		    if not os.access('.', os.W_OK):
			print "Unable to create database file %s" % (self.dbfile)
			exit(1)
		return status

	def sql(self, sql, params=()):
		''' Method to connect and execute some SQL sentence '''
		data = None
		try:
			self.con = lite.connect(self.dbfile)
			cur = self.con.cursor()
			cur.execute(sql, params)
			self.con.commit()
			data = cur.fetchall()
		except lite.Error, e:
			print "Error in sql => %s" % e.args[0]
			#sys.exit(1)
		finally:
			if self.con is not None:
				self.con.close()
		return data

	def create_table(self):
		return self.sql("""CREATE TABLE banned \
	(ip, \
	try DEFAULT 0, \
	block DEFAULT 0, \
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP, \
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)""")

	def show_ips(self):
	  return self.sql("SELECT ip, try, block, created_at, updated_at FROM banned")

	def show_blocked(self):
	    ips = self.sql("SELECT ip FROM banned WHERE block = 1")
	    response = []
	    type(ips)
	    for ip in ips:
		response.append(ip[0])
	    return response

	def insert_ip(self, ip, ntry=1):
		''' Method to insert the IP into the table of banned ips '''
		existe = self.sql("SELECT try FROM banned WHERE ip = ?", (ip,))
		tries = 1
		if len(existe) is 0:
			existe = self.sql("INSERT INTO banned (ip) VALUES (?)", (ip, ))
		else:
			tries = int(existe[0][0]) + ntry
			existe = self.sql("""UPDATE banned
												SET updated_at=DATETIME('now'), try=? WHERE ip=?""",
				    						(tries, ip, ))
		return tries

	def block_ip(self, ip):
		done = False
		db.insert_ip(ip, 0)
		res = self.sql("""UPDATE banned SET updated_at=DATETIME('now'), block = 1
						WHERE ip=?""", (ip, ))
		if res is not None:
			done = True
		return done

	def unblock_ip(self, ip):
		done = False
		db.insert_ip(ip, 0)
		res = self.sql("""UPDATE banned SET updated_at=DATETIME('now'), block = 0
									WHERE ip=?""", (ip, ))
		if res is not None:
			done = True
		return done

	def delete_ip(self, ip):
		done = False
		db.insert_ip(ip, 0)
		res = self.sql("DELETE FROM banned WHERE ip=?", (ip, ))
		if res is not None:
			done = True
		return done

if __name__ == '__main__':
	ip1 = "192.168.1.2"
	ip2 = "192.168.1.3"
	db = DB('sipcheck.db')
	db.create_table()
	print db.show_blocked()
	print "Intentos: %r" % db.insert_ip(ip1)
	print db.show_ips()
	print db.block_ip(ip1)
	print db.unblock_ip(ip1)
	print db.block_ip(ip2)
	print db.delete_ip(ip2)
