"""Weixin OAuth 2.0 Requests, trade code for token.

.. moduleauthor:: Tsai Phan <phanalpha@hotmail.com>
"""

from urlrequest import URLRequest
from str_enum import StrEnum, value_of
from credential import Credential


class GrantType(StrEnum):
    AUTHORIZATION_CODE = 'authorization_code'
    REFRESH_TOKEN = 'refresh_token'


class TokRequest(URLRequest):
    """Token request.
    """

    def __init__(self, url, app, grant_type):
        """Token request.

        Args:
            url (str): url sample.
            app (WxApp): Weixin app.
            grant_type (str): OAuth 2.0 grant type.
        """
        super(TokRequest, self).__init__(url)

        self.app = app
        self.grant_type = grant_type

    def build(self):
        return dict(
            appid=self.app.id,
            grant_type=value_of(self.grant_type)
        )

    def commit(self):
        """
        Returns:
            Credential.
        """
        res = super(TokRequest, self).commit()

        return Credential(
            access_token=res['access_token'],
            expire_in=res['expires_in'],
            refresh_token=res['refresh_token'],
            openid=res['openid'],
            scope=filter(None, res['scope'].split(',')),
            unionid=res.get('unionid')
        )


class AccessRequest(TokRequest):
    """Access request, trade authorization code for access token.
    """

    def __init__(self, app, code):
        """Access request.

        .. seealso:: TokRequest
        """
        super(AccessRequest, self).__init__(
            'https://api.weixin.qq.com/sns/oauth2/access_token'
            '?appid=APPID'
            '&secret=SECRET'
            '&code=CODE'
            '&grant_type=authorization_code',
            app,
            GrantType.AUTHORIZATION_CODE
        )

        self.code = code

    def build(self):
        return dict(
            super(AccessRequest, self).build(),
            code=self.code,
            secret=self.app.secret
        )


class RefreshRequest(TokRequest):
    """Refresh request, refresh access token with refresh token.
    """

    def __init__(self, app, credential):
        """Refresh request.

        .. seealso:: TokRequest
        """
        super(RefreshRequest, self).__init__(
            'https://api.weixin.qq.com/sns/oauth2/refresh_token'
            '?appid=APPID'
            '&grant_type=refresh_token'
            '&refresh_token=REFRESH_TOKEN',
            app,
            GrantType.REFRESH_TOKEN
        )

        self.credential = credential

    def build(self):
        return dict(
            super(RefreshRequest, self).build(),
            refresh_token=self.credential.refresh_token
        )
