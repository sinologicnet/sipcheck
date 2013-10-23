#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser,os

class ConfigFile:

  def __init__(self,archivo):
	config = ConfigParser.ConfigParser()
	config.read(archivo)

	# Get the message file of Asterisk where it is storaged with all notices and warnings messages
	try:
	  self.messagefile=config._sections['general']['messagefile']
	except KeyError:
	  print "Fatal Error: messagefile parameter not found in",archivo
	  exit(1)

