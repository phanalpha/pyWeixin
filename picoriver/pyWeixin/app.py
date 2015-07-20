import os
import base64

from authrequest import LoginRequest


class App(object):
    def __init__(self, id, secret):
        self.id = id
        self.secret = secret


    def request_login(self, redirect_url, state=None):
        if state is None:
            state = base64.urlsafe_b64encode(os.urandom(36))

        return LoginRequest(self, redirect_url, state), state


    def login(self, code):
        pass
