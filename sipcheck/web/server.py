# -*- coding: UTF-8 -*-

from flask.views import MethodView
from flask import render_template
from sipcheck.web.web_auth import WebAuth

web_auth = WebAuth()

class ServerAPI(MethodView):

    def __init__(self, user, passwd):
        web_auth.set_login_info(user, passwd)

    @web_auth.requires_auth
    def get(self):
        return render_template('server_status.html')

    @web_auth.requires_auth
    def post(self):
        print "post!"

