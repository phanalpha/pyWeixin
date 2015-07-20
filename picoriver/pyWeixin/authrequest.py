"""Weixin OAuth 2.0 Requests, initiate authorization.

.. moduleauthor:: Tsai Phan <phanalpha@hotmail.com>
"""

from urlrequest import URLRequest
from str_enum import StrEnum, value_of


class ResponseType(StrEnum):
    """response_type options.
    """

    CODE = 'code'


class Scope(StrEnum):
    """scope options.
    """

    ID = 'snsapi_base'
    LOGIN = 'snsapi_login'
    PROFILE = 'snsapi_userinfo'


class AuthRequest(URLRequest):
    def __init__(self, url, app, redirect_url, response_type, scope, state):
        super(AuthRequest, self).__init__(url)

        self.app = app
        self.redirect_url = redirect_url
        self.response_type = response_type
        self.scope = scope
        self.state = state

    def __str__(self):
        return str(self.query(
            appid=self.app.id,
            redirect_uri=self.redirect_url,
            response_type=value_of(self.response_type),
            scope=value_of(self.scope),
            state=self.state
        ))


class DirectAuthRequest(AuthRequest):
    def __init__(self, app, redirect_url, response_type, scope, state):
        super(DirectAuthRequest, self).__init__(
            'https://open.weixin.qq.com/connect/oauth2/authorize'
            '?appid=APPID'
            '&redirect_uri=REDIRECT_URI'
            '&response_type=code'
            '&scope=SCOPE'
            '&state=STATE'
            '#wechat_redirect',
            app,
            redirect_url,
            response_type,
            scope,
            state
        )


class IndirectAuthRequest(AuthRequest):
    def __init__(self, app, redirect_url, response_type, scope, state):
        super(IndirectAuthRequest, self).__init__(
            'https://open.weixin.qq.com/connect/qrconnect'
            '?appid=APPID'
            '&redirect_uri=REDIRECT_URI'
            '&response_type=code'
            '&scope=SCOPE'
            '&state=STATE'
            '#wechat_redirect',
            app,
            redirect_url,
            response_type,
            scope,
            state
        )


class GrantRequest(IndirectAuthRequest):
    def __init__(self, app, redirect_url, state):
        super(GrantRequest, self).__init__(
            app,
            redirect_url,
            ResponseType.CODE,
            Scope.LOGIN,
            state
        )
