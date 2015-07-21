"""Weixin open / mp OAuth 2.0.

.. moduleauthor:: Tsai Phan <phanalpha@hotmail.com>
"""

import os
import base64

from authrequest import LoginRequest
from tokrequest import AccessRequest, RefreshRequest


class WxApp(object):
    """A open / mp Weixin app identified by (AppID, AppSecret).

    .. seealso:: <https://open.weixin.qq.com/>
                 <https://mp.weixin.qq.com/>
    """

    def __init__(self, appid, secret):
        """App with appid and secret.

        Args:
            appid (str): AppID
            secret (str): AppSecret
        """
        self.id = appid
        self.secret = secret

    def login(self, redirect_uri, state=None):
        """Initiate login authorization.

        The URLRequest could be committed in a client-side browser,
        in order to initiate the auth. End-user might interact via
        (scanning) QrCode or so.

        Args:
            redirect_uri (str): uri to direct resource owner's user-agent back
                                after completing its interaction.

        Kwargs:
            state (str): an opaque value to maintain state
                         between the request and callback.

        Returns:
            A tuple with URLRequest, and the state.
        """
        if state is None:
            state = base64.urlsafe_b64encode(os.urandom(36))

        return LoginRequest(self, redirect_uri, state), state

    def access(self, code):
        """Trade code for access token.

        Args:
            code (str): authorization code.

        Returns:
            Credential, access token and refresh token or so.
        """
        return AccessRequest(self, code).commit()

    def refresh(self, credential):
        """Refresh access token.
        Args:
            credential (Credential): credential, mostly refresh token.

        Returns:
            New credential, access token refreshed.
        """
        return RefreshRequest(self, credential).commit()
