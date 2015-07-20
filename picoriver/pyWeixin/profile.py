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
    def __new__(cls, openid, nickname, portrait, gender,
                province, city, country, privileges, unionid):
        return super(Profile, cls).__new__(
            openid,
            nickname,
            portrait,
            gender,
            province,
            city,
            country,
            privileges,
            unionid
        )
