#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Flask

app = Flask(__name__)

class WebUI(object):

    def __init__(self):
        app.debug = True
        app.run()

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    @app.route('/server/stop')
    def server_stop():
        return "Stoping Server"

