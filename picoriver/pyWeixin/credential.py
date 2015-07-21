"""Access token and refresh token, openid or so.

.. moduleauthor:: Tsai Phan <phanalpha@hotmail.com>
"""

from datetime import datetime, timedelta
from collections import namedtuple
from exception import WxException

from resrequest import AuthenticationRequest, ProfileRequest


class Credential(namedtuple('POCredential', [
        'access_token',
        'expire_at',
        'refresh_token',
        'openid',
        'scope',
        'unionid'
])):
    """Credential, access token and refresh token, openid or so.
    """

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
        """Authenticate credential.

        Raises:
            WxException: authentication error, message and code.
        """
        AuthenticationRequest(self).commit()

    def is_valid(self):
        """Validate credential.

        Returns:
            True on valid, or False.
        """
        try:
            self.authenticate()

            return True

        except WxException:
            return False

    def profile(self):
        """User profile.

        Returns:
            Profile.

        Raises:
            WxException: access error, message and code.
        """
        return ProfileRequest(self).commit()
