"""StrEnum, and util.

.. moduleauthor:: Tsai Phan <phanalpha@hotmail.com>
"""

from enum import Enum


class StrEnum(str, Enum):
    pass


def value_of(e):
    return isinstance(e, Enum) and e.value or e
