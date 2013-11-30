# -*- coding: UTF-8 -*-

from flask.views import MethodView
from flask import render_template
from sipcheck.web.web_auth import WebAuth

web_auth = WebAuth()

class BanAPI(MethodView):

    def __init__(self, bandb, user, passwd):
        web_auth.set_login_info(user, passwd)
        self.bandb = bandb

    @web_auth.requires_auth
    def get(self, ip=None):
        return render_template('bans.html', bans=self.bandb.show_ips())

    @web_auth.requires_auth
    def put(self, ip, block):
        print "put!"
        return "ok"

    @web_auth.requires_auth
    def delete(self, ip):
        print "delete!"
        return "ok"
