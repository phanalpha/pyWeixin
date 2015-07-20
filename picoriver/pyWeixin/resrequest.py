from urlrequest import URLRequest
from contextlib import closing
from exception import WxException
from profile import Profile

import urllib2
import json


class ValidationRequest(URLRequest):
    def __init__(self, credential):
        super(ValidationRequest).__init__(
            'https://api.weixin.qq.com/sns/auth'
            '?access_token=ACCESS_TOKEN'
            '&openid=OPENID'
        )

        self.credential = credential

    def commit(self):
        with closing(urllib2.urlopen(
                str(self.query(
                    access_token=self.credential.access_token,
                    openid=self.credential.openid
                ))
        )) as f:
            res = json.loads(f.read())

        if res.get('errcode'):
            raise WxException(res['errmsg'], res['errcode'])


class ProfileRequest(URLRequest):
    def __init__(self, credential):
        super(ProfileRequest, self).__init__(
            'https://api.weixin.qq.com/sns/userinfo'
            '?access_token=ACCESS_TOKEN'
            '&openid=OPENID'
        )

        self.credential = credential

    def commit(self):
        with closing(urllib2.urlopen(
                str(self.query(
                    access_token=self.credential.access_token,
                    openid=self.credential.openid
                ))
        )) as f:
            res = json.loads(f.read())

        if res.get('errcode'):
            raise WxException(res['errmsg'], res['errcode'])

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
