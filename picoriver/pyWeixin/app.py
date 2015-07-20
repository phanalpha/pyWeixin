"""Weixin open / mp OAuth 2.0.

.. moduleauthor:: Tsai Phan <phanalpha@hotmail.com>
"""

import os
import base64

from authrequest import GrantRequest
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

    def auth(self, redirect_url, state=None):
        """Initiate OAuth 2.0 authorization.

        The URLRequest could be committed in a client-side browser,
        in order to initiate the auth. End-user might interact via
        (scanning) QrCode or so.

        Args:
            redirect_url (str): url to redirect on user acknowledged

        Kwargs:
            state (str): data postback along with
                         (authorization) code (if available)

        Returns:
            A tuple with URLRequest, and the state.
        """
        if state is None:
            state = base64.urlsafe_b64encode(os.urandom(36))

        return GrantRequest(self, redirect_url, state), state

    def access(self, code):
        """Trade code for access token.

        Args:
            code (str): authorization code

        Returns:
            Credential, access token and refresh token or so.

        Raises:
            WxException: error message and code from Weixin
        """
        return AccessRequest(self, code).commit()

    def refresh(self, credential):
        """Refresh access token.
        Args:
            credential (Credential): credential, mostly refresh token.

        Returns:
            New credential, access token refreshed.

        Raises:
            WxException: error message and code from Weixin
        """
        return RefreshRequest(self, credential).commit()
