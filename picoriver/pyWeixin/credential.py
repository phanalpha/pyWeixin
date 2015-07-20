from datetime import datetime, timedelta
from collections import namedtuple
from exception import WxException

from resrequest import ValidationRequest, ProfileRequest


class Credential(namedtuple('POCredential', [
        'access_token',
        'expire_at',
        'refresh_token',
        'openid',
        'scope',
        'unionid'
])):
    def __new__(cls, access_token, expire_in,
                refresh_token, openid, scope, unionid):
        return super(Credential, cls).__new__(
            cls,
            access_token,
            datetime.utcnow() + timedelta(seconds=expire_in),
            refresh_token,
            openid,
            scope,
            unionid,
        )

    def authenticate(self):
        ValidationRequest(self).commit()

    def is_valid(self):
        try:
            self.authenticate()

            return True

        except WxException:
            return False

    def profile(self):
        return ProfileRequest(self).commit()
