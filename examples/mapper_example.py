#from auto_pdb import activate_crash_pdb
#activate_crash_pdb(key_interrupts=False)

from lollygag import run
from lollygag import MapperCrawler, Services, LinkParser, DomainCrawler, Crawler


class MyParser(LinkParser):
    def __init__(self, *args, **kwargs):
        super(MyParser, self).__init__(*args, **kwargs)
        self.use_next_data = False

    # on new page is found and shall be processed, 'data' contains full html-source
    def feed(self, data):
        return super(MyParser, self).feed(data)

    # on each start-tag found inside the full html-source
    def handle_starttag(self, tag, attrs):
        # super() will handle links (<a>) parsing, you can add() arbitrary links to self._links
        super(MyParser, self).handle_starttag(tag, attrs)

        # <img> tag found, report/keep it...
        if tag == "img":
            pass
            #self.log_service.info("[image] => {}".format(
            #    dict(attrs).get("src", "<no src attr>")))

        # <a> tag for logging...
        elif tag == "a":
            #self.log_service.info("[link]  => {}".format(
            #    dict(attrs).get("href", "<no href attr>")))
            pass

    # on each data (between two tags)
    def handle_data(self, data):
        pass

    # on each end-tag found
    def handle_endtag(self, tag):
        pass





# `Services.site_parser_factory` defines how a single page is parsed
Services.site_parser_factory = MyParser

# set `crawler_factory` and set 'max_depth' for crawling
MapperCrawler.max_depth = 2
Services.crawler_factory = MapperCrawler
# before crawling, let's subscribe to some crawler events:
# 3 events may get callbacks (with following function-prototypes):
# - on_start(url)
# - on_interrupt()
# - on_finish(visited_urls, urls_in_progress, urls_to_crawl)
callbacks = {
    "on_start": lambda url: print("[START] crawling: {}".format(url)),
    "on_interrupt": lambda: print("[INTERRUPTED]"),
    "on_finish": lambda visited, ongoing, todo: \
        print("\n[FINISH] #seen: {},\n #ongoing: {},\n #todo: {}".format(
            len(visited), len(ongoing), len(todo)))
}

# now start
run(subscribe=callbacks)
