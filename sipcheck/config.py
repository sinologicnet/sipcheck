# -*- coding: utf-8 -*-
'''
    Read & parse config file
'''

import ConfigParser

class Config(object):
    ''' Read & parse config file '''

    def __init__(self, config_file):
        ''' consutructor '''
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_file)

    def get_general(self, key):
        ''' Return value of general config '''
        return self.config.get('general', key)

    def get_shared(self, key):
        ''' Return value of shared config '''
        return self.config.get('shared', key)

    def get_database(self, key):
        ''' Return value of database config '''
        return self.config.get('database', key)

    def get_ignore(self):
        ''' Return ip ranges to ignore '''
        return self.config.get('ignore', 'own').split(',')

    def get_gui(self, key):
        ''' Return value of database config '''
        return self.config.get('gui', key)
