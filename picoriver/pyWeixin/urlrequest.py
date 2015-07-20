from urllib import urlencode
from urlparse import urlparse, urlunparse, ParseResult


class URLRequest(object):
    def __init__(self, url):
        self.url = isinstance(url, ParseResult) and url or urlparse(url)

    def query(self, **kwargs):
        return URLRequest(ParseResult(
            self.url.scheme,
            self.url.netloc,
            self.url.path,
            self.url.params,
            urlencode(kwargs),
            self.url.fragment
        ))

    def __str__(self):
        return urlunparse(self.url)
