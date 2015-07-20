"""Weixin OAuth 2.0 Requests, trade code for token.

.. moduleauthor:: Tsai Phan <phanalpha@hotmail.com>
"""

from urlrequest import URLRequest
from str_enum import StrEnum, value_of
from contextlib import closing
from credential import Credential
from exception import WxException

import urllib2
import json


class GrantType(StrEnum):
    AuthorizationCode = 'authorization_code'
    RefreshToken = 'refresh_token'


class TokRequest(URLRequest):
    def __init__(self, url, app, grant_type):
        super(TokRequest, self).__init__(url)

        self.app = app
        self.grant_type = grant_type

    def build(self):
        return dict(
            appid=self.app.id,
            grant_type=value_of(self.grant_type)
        )

    def commit(self):
        with closing(urllib2.urlopen(str(self.query(**self.build())))) as f:
            res = json.loads(f.read())

        if res.get('errcode'):
            raise WxException(res['errmsg'], res['errcode'])

        return Credential(
            access_token=res['access_token'],
            expire_in=res['expires_in'],
            refresh_token=res['refresh_token'],
            openid=res['openid'],
            scope=filter(None, res['scope'].split(',')),
            unionid=res.get('unionid')
        )


class AccessRequest(TokRequest):
    def __init__(self, app, code):
        super(AccessRequest, self).__init__(
            'https://api.weixin.qq.com/sns/oauth2/access_token'
            '?appid=APPID'
            '&secret=SECRET'
            '&code=CODE'
            '&grant_type=authorization_code',
            app,
            GrantType.AuthorizationCode
        )

        self.code = code

    def build(self):
        return dict(
            super(AccessRequest, self).build(),
            code=self.code,
            secret=self.app.secret
        )


class RefreshRequest(TokRequest):
    def __init__(self, app, credential):
        super(RefreshRequest, self).__init__(
            'https://api.weixin.qq.com/sns/oauth2/refresh_token'
            '?appid=APPID'
            '&grant_type=refresh_token'
            '&refresh_token=REFRESH_TOKEN',
            app,
            GrantType.RefreshToken
        )

        self.credential = credential

    def build(self):
        return dict(
            super(RefreshRequest, self).build(),
            refresh_token=self.credential.refresh_token
        )
