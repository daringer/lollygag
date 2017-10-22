"""
Holds the ConfigService service.
"""
from lollygag.dependency_injection.inject import Inject
from lollygag.dependency_injection.requirements import HasMethods

DEFAULT_CONFIG = {
    'threads': 10,
    'loglevel': 'all',
    'urls': '',
    'skip': [
        r'\.pdf$',
        r'\.jpg$',
        r'\.png$',
        r'\.jpeg$',
        "^#",
        r"\.css$",
        r"\.ico$",
        r"\.docx?$",
        r"\.xlsx?$"
    ]
}


class ConfigService(object):
    """
    Stores configuration details.
    Parses arguments in argumentParser on construction.
    Arguments not in argumentParser will fall back to the DEFAULT_CONFIG.
    Implements the Borg pattern so all instances share state with the class itself.
    """
    argumentParser = Inject("argparse", HasMethods("add_argument", "parse_args"))
    state = {}

    threads = DEFAULT_CONFIG['threads']
    loglevel = DEFAULT_CONFIG['loglevel']
    urls = DEFAULT_CONFIG['urls']
    skip = DEFAULT_CONFIG['skip']

    def __init__(self):
        self.__dict__ = ConfigService.state

    def setup(self):
        """
        Initialize ConfigService.state if it hasn't been already.
        Parses args from the standard input.
        """
        if not ConfigService.state:
            self.__init_args()
            args = self.argumentParser.parse_args().__dict__
            ConfigService.state.update(args)

    def __init_args(self):
        avail_logs = ["all", "debug", "info", "warn", "error", "none"]
        helps = {
            'urls': "Base url(s) you wish to crawl",
            'threads': "Maximum number of concurrent threads",
            'loglevel': "Level of logging [{}]".format(", ".join(avail_logs)),
            'skip': "Regex patterns, when any of them is found in the url, it's skipped",
            'verify-ssl': "Certificates for https:// urls are verified"
        }
        self.argumentParser.add_argument("urls", nargs="*", metavar="urls", 
                                         action="append", help=helps['urls'])
        self.argumentParser.add_argument("--urls", "-u", nargs="*", metavar="urls", 
                                         action="append", help=helps['urls'] + " (legacy)")

        self.argumentParser.add_argument("--threads", "-t", nargs="?", const=int,
                                         default=DEFAULT_CONFIG['threads'],
                                         help=helps['threads'], required=False)
        self.argumentParser.add_argument("--loglevel", "-l", choices=avail_logs,
                                         default=DEFAULT_CONFIG['loglevel'],
                                         help=helps['loglevel'], required=False)
        self.argumentParser.add_argument("--skip", "-s",
                                         default=DEFAULT_CONFIG['skip'],
                                         help=helps['skip'], required=False)
