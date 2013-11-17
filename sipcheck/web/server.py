# -*- coding: UTF-8 -*-

from flask.views import MethodView
from flask import render_template

class ServerAPI(MethodView):

    def get(self):
        return render_template('server_status.html')


    def post(self):
        print "post!"

