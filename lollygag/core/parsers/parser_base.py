from collections import namedtuple
from lollygag.dependency_injection.inject import Inject
from lollygag.dependency_injection.requirements import HasMethods

ParseResult = namedtuple("ParseResult", ["link", "status_code", "page_size"])

class Parser(object):
    """
    Base class for parsers
    The parser performs a GET request on the url and calls feed with the response.text
    Subclasses should implement the feed method
    """
    _requests = Inject("requests", HasMethods("get"))
    log_service = Inject("log_service", HasMethods("debug", "info", "error", "warn"))

    def crawl(self, url):
        assert url is not None
        response = self._requests.get(url, verify=False)
        if response.status_code == 200:
            self.feed(response.text)
        return ParseResult(link=url, status_code=response.status_code \
            , page_size=len(response.content))

    def feed(self, data):
        pass