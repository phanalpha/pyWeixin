"""Resource requests.

.. moduleauthor:: Tsai Phan <phanalpha@hotmail.com>
"""

from urlrequest import URLRequest
from contextlib import closing
from exception import WxException
from profile import Profile

import urllib2
import json


class ResourceRequest(URLRequest):
    """Resource request, access via credential.
    """

    def __init__(self, url, credential):
        """Resource request.

        Args:
            url (str): url sample.
            credential (Credential): access token or so.
        """
        super(ResourceRequest, self).__init__(url)

        self.credential = credential

    def build(self):
        return dict(
            access_token=self.credential.access_token,
            openid=self.credential.openid
        )


class AuthenticationRequest(ResourceRequest):
    """Credential (token) authentication request.
    """

    def __init__(self, credential):
        super(AuthenticationRequest, self).__init__(
            'https://api.weixin.qq.com/sns/auth'
            '?access_token=ACCESS_TOKEN'
            '&openid=OPENID',
            credential
        )


class ProfileRequest(ResourceRequest):
    """Profile request.
    """

    def __init__(self, credential):
        super(ProfileRequest, self).__init__(
            'https://api.weixin.qq.com/sns/userinfo'
            '?access_token=ACCESS_TOKEN'
            '&openid=OPENID',
            credential
        )

    def commit(self):
        """
        Returns:
            Profile.
        """
        res = super(ProfileRequest, self).commit()

        return Profile(
            openid=res['openid'],
            nickname=res['nickname'],
            portrait=res['headimgurl'],
            gender=res['sex'],
            province=res['province'],
            city=res['city'],
            country=res['country'],
            privileges=res['privilege'],
            unionid=res['unionid']
        )
