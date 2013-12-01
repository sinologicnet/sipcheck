# -*- coding: UTF-8 -*-

from flask.views import MethodView
from flask import request
from flask import render_template
from sipcheck.web.web_auth import WebAuth

web_auth = WebAuth()

class BanAPI(MethodView):

    def __init__(self, bandb, user, passwd):
        web_auth.set_login_info(user, passwd)
        self.bandb = bandb

    @web_auth.requires_auth
    def get(self, ip):
        return render_template('bans.html', bans=self.bandb.show_ips())

    @web_auth.requires_auth
    def put(self, ip):
        if request.form['block'] == 'true':
            self.bandb.block_ip(ip)
        else:
            self.bandb.unblock_ip(ip)
        return "ok"

    @web_auth.requires_auth
    def delete(self, ip):
        done = self.bandb.delete_ip(ip)
        return "ok" if done else "ko"
