from flask import request
from flask import Response
from functools import wraps

class WebAuth(object):

    def __init__(self):
        self.user = 'admin'
        self.passwd = '1234'

    def set_login_info(self, user, passwd):
        self.user = user
        self.passwd = passwd

    def check_auth(self, username, password):
        """This function is called to check if a username /
        password combination is valid.
        """
        return  username == self.user and password == self.passwd


    def authenticate(self):
        """Sends a 401 response that enables basic auth"""
        return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

    def requires_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not self.check_auth(auth.username, auth.password):
                return self.authenticate()
            return f(*args, **kwargs)
        return decorated
