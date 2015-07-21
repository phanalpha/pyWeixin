"""Weixin errors, message and code.

.. moduleauthor:: Tsai Phan <phanalpha@hotmail.com>
"""

class WxException(Exception):
    """Weixin error.
    """

    def __init__(self, message, code):
        """Weixin error.

        Args:
            message (str): error message.
            code (int): error code.
        """
        super(WxException, self).__init__(message)

        self.code = code
