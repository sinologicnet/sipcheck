#!/usr/bin/env python -B
# -*- coding: utf-8 -*-


import ConfigParser,os

class ConfigFile:

  def __init__(self,archivo):
	config = ConfigParser.ConfigParser()
	config.read(archivo)

	# Get the message file of Asterisk where it is storaged with all notices and warnings messages
#	try:

	self.messagefile=config._sections['general']['messagefile']
	self.debug=config._sections['general']['debug']
	self.minticks=config._sections['general']['minticks']
	self.messagebuffer=config._sections['general']['messagebuffer']
	self.logfile=config._sections['general']['logfile']
	self.username=config._sections['general']['username']
	self.password=config._sections['general']['password']

	if "yes" in config._sections['general']['useiptables'].lower():
	    self.iptables=True
	else:
	    self.iptables=False

	    
#	except KeyError:
#	  print "Fatal Error: messagefile parameter not found in",archivo
#	  exit(1)

