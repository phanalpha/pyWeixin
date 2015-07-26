"""User profile, nickname and portrait or so.

.. moduleauthor:: Tsai Phan <phanalpha@hotmail.com>
"""

from collections import namedtuple
from enum import IntEnum


Gender = IntEnum('Gender', 'MALE FEMALE')


class Profile(namedtuple('POProfile', [
        'openid',
        'nickname',
        'portrait',
        'gender',
        'province',
        'city',
        'country',
        'privileges',
        'unionid',
])):
    """User profile, openid, nickname, portrait, gender and more.
    """

    @property
    def id(self):
        return self.unionid
