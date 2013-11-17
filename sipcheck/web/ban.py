# -*- coding: UTF-8 -*-

from flask.views import MethodView
from flask import render_template

class BanAPI(MethodView):

    def __init__(self, bandb):
        self.bandb = bandb

    def get(self):
        return render_template('bans.html', bans=self.bandb.show_ips())


    def post(self):
        print "post!"

