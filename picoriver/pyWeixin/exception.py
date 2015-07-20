"""Weixin errors, message and code.

.. moduleauthor:: Tsai Phan <phanalpha@hotmail.com>
"""

class WxException(Exception):
    def __init__(self, message, code):
        super(WxException, self).__init__(message)
        self.code = code
