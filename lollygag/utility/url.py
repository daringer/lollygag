"""
Holds functionality to process urls.
"""
import re


REGEX_REL = re.compile(r"^[\.\/]*\??\#?([A-Za-z0-9\.&=:\-])*")
REGEX_DOMAIN = re.compile(r"(^https?://)?([a-zA-Z0-9\.\-]+)/?")
REGEX_PROTO = re.compile(r"^https?://")

def get_protocol(url):
    """
    Returns wether the protocol of the url is http or https.
    Returns none if another protocol or no protocol is present in the url.
    """
    result = REGEX_PROTO.search(url)
    return result.group(0) if result else None

def strip_beginning_slashes(url):
    """
    Removes unnecessary slashes from the beginning of the url.
    """
    find = re.search(r"^/+", url)
    if find:
        url = re.sub(find.group(0), "", url)
    return url

def get_domain(url):
    """
    Returns the domain of the given url.
    Examples:
        get_domain("http://winnie.thepooh") -> "winnie.thepooh"

        get_domain("http://www.winnie.thepooh") -> "winnie.thepooh"

        get_domain("http://www.winnie.thepooh/") -> "winnie.thepooh"
    """
    assert url is not None
    protocol = get_protocol(url)
    find = REGEX_DOMAIN.search(url)
    result = None
    if find:
        result = find.group(0)
        if result.endswith("/"):
            result = result[0:-1]
        result = result.replace("www.", "")
        if protocol:
            result = result.replace(protocol, "")
    return result

def is_usable_link(link):
    """
    Returns a boolean to determine,
    if link is usable / suitable for crawling
    """
    if link in [None, False, True]:
        return False

    if link.startswith("http"):
        return True

    # anchor only-links are considered useless
    if link.startswith("#"):
        return False

    # any 'bad' protocol is also useless:
    # - assumption that a ":" is always marking the end, this is the distinguishing symbol!
    if re.match(r"^(ftp|mailto|javascript|chrome|tv|[a-zA-Z]+):", link):
        return False
    return True

def is_relative_link(link):
    """
    Returns wether the passed link is a relative link or not.
    'relative' means here: any path which does not contain a domain/protocol.
    """

    # mmmh, seems simple, but correct (?) incl. the other extreme...
    if not "/" in link or link == "/":
        return True
    return not get_protocol(link) and REGEX_REL.match(link)
