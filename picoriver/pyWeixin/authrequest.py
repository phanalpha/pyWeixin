"""Weixin OAuth 2.0 Requests, initiate login authorization.

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
    """Authorization request, a base class.
    """

    def __init__(self, url, app, redirect_uri, response_type, scope, state):
        """Generic authorization request.

        Args:
            url (str): url sample.
            app (WxApp): Weixin app.
            redirect_uri (str): url to redirect on user acknowledged.
            response_type (ResponseType): OAuth 2.0 response type.
            scope (Scope): access token scope.
            state (str): an opaque value to maintain state
                         between the request and callback.
        """
        super(AuthRequest, self).__init__(url)

        self.app = app
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.scope = scope
        self.state = state

    def __str__(self):
        return str(self.query(
            appid=self.app.id,
            redirect_uri=self.redirect_uri,
            response_type=value_of(self.response_type),
            scope=value_of(self.scope),
            state=self.state
        ))


class DirectAuthRequest(AuthRequest):
    """In Weixin (mobile) app authorize request.
    """

    def __init__(self, app, redirect_uri, response_type, scope, state):
        """In Weixin authorization request.

        .. seealso:: AuthRequest
        """
        super(DirectAuthRequest, self).__init__(
            'https://open.weixin.qq.com/connect/oauth2/authorize'
            '?appid=APPID'
            '&redirect_uri=REDIRECT_URI'
            '&response_type=code'
            '&scope=SCOPE'
            '&state=STATE'
            '#wechat_redirect',
            app,
            redirect_uri,
            response_type,
            scope,
            state
        )


class IndirectAuthRequest(AuthRequest):
    """QrCode (scanning) Weixin authorization request.
    """

    def __init__(self, app, redirect_uri, response_type, scope, state):
        """QrCode Weixin authorization request.

        .. seealso:: AuthRequest
        """
        super(IndirectAuthRequest, self).__init__(
            'https://open.weixin.qq.com/connect/qrconnect'
            '?appid=APPID'
            '&redirect_uri=REDIRECT_URI'
            '&response_type=code'
            '&scope=SCOPE'
            '&state=STATE'
            '#wechat_redirect',
            app,
            redirect_uri,
            response_type,
            scope,
            state
        )


class LoginRequest(IndirectAuthRequest):
    """Weixin login (QrCode) authorization request.
    """

    def __init__(self, app, redirect_uri, state):
        """Weixin login authorization request.

        .. seealso:: AuthRequest
        """
        super(LoginRequest, self).__init__(
            app,
            redirect_uri,
            ResponseType.CODE,
            Scope.LOGIN,
            state
        )
