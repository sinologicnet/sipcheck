# -*- coding: UTF-8 -*-

from flask import Flask
from .web.ban import BanAPI
from .web.server import ServerAPI
from .config import Config
from .db import DB

class WebUI(object):

    def __init__(self, config_file):
        app = Flask(__name__, template_folder="web/templates")

        self.config = Config(config_file)
        self.ip_dbs = self.init_db(self.config.get_database('file'))

        app.debug = True
        app.add_url_rule('/bans/',
                         view_func=BanAPI.as_view('bans', bandb=self.ip_dbs))
        app.add_url_rule('/server/', view_func=ServerAPI.as_view('servers'))
        app.run()


    def init_db(self, dbfile):
        ''' Init database '''
        bdb = DB(dbfile)
        if bdb.exists() is not True:
            return None
        return bdb
