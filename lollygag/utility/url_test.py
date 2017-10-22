import unittest
from lollygag.utility.url import get_domain 
from lollygag.utility.url import is_relative_link as is_rel
from lollygag.utility.url import is_usable_link as is_link

class get_domainTest(unittest.TestCase):
    def test_should_recognise_http(self):
        result = get_domain("http://winnie.thepooh")
        self.assertEqual(result, "winnie.thepooh")

    def test_should_recognise_https(self):
        result = get_domain("https://winnie.thepooh")
        self.assertEqual(result, "winnie.thepooh")

    def test_should_remove_www(self):
        result = get_domain("http://www.winnie.thepooh")
        self.assertEqual(result, "winnie.thepooh")

    def test_should_remove_last_per(self):
        result = get_domain("http://www.winnie.thepooh/")
        self.assertEqual(result, "winnie.thepooh")
    
    def test_domain_with_dash(self):
        result = get_domain("http://www.hello-i-am-evil.com/foo.html")
        self.assertEqual(result, "hello-i-am-evil.com")
    
    def test_should_recognise_ip(self):
        result = get_domain("http://123.125.255.1")
        self.assertEqual(result, "123.125.255.1")

    def test_raises_on_None(self):
        with self.assertRaises(AssertionError):
            get_domain(None)

class is_relative_or_usable_link(unittest.TestCase):
    def setUp(self):
        self.proto = "http://"
        self.bad_proto = ["ftp://", "mailto://", "tv://", "weird://", "alpha://"]
        self.good_proto = ["https://", self.proto]
    
    ### here 'is_link()' and 'is_rel()' tests combined, due to the obvious co-impacts...
    def test_is_not_usable_link_anchor(self):
        self.assertFalse(is_link("#foo"))
        self.assertFalse(is_link("#"))
    
    def test_is_not_usable_link_proto(self):
        self.assertTrue(not any(is_link(p) for p in self.bad_proto))

    def test_is_rel_url_abs_path(self):
        self.assertTrue(is_rel("/"))
        self.assertTrue(is_link("/"))
        self.assertTrue(is_rel("/myfile.php"))
        self.assertTrue(is_link("/myfile.php"))

    def test_is_rel_url_rel_path(self):
        self.assertTrue(is_rel("target.html"))
        self.assertTrue(is_link("target.html"))
        self.assertTrue(is_rel(""))
        self.assertTrue(is_link(""))

    def test_is_rel_url_options_abs(self):
        self.assertTrue(is_rel("/?myname=somevalue&blub=bla"))
        self.assertTrue(is_link("/?"))
        self.assertTrue(is_rel("/?myname=somevalue&blub=bla"))
        self.assertTrue(is_link("/?"))

    def test_is_rel_url_options_rel(self):
        self.assertTrue(is_rel("?myname=somevalue&blub=bla"))
        self.assertTrue(is_rel("?"))
        self.assertTrue(is_link("?myname=somevalue&blub=bla"))
        self.assertTrue(is_link("?"))

    def test_is_rel_url_anchor(self):
        self.assertTrue(is_rel("#something"))
        self.assertTrue(is_rel("#"))
        self.assertFalse(is_link("#something"))
        self.assertFalse(is_link("#"))

    def test_is_not_rel_url_proto_simple(self):
        self.assertFalse(is_rel(self.proto))
        self.assertTrue(is_link(self.proto))

    def test_is_rel_url_valid_proto(self):
        for prot in self.good_proto:
            self.assertFalse(is_rel(prot))
            self.assertTrue(is_link(prot))

    def test_is_not_rel_url_proto_path(self):
        self.assertFalse(is_rel(self.proto + "mydomain.com/index.html"))
        self.assertFalse(is_rel(self.proto + "mydomain.com:80/index.html"))
        self.assertFalse(is_rel(self.proto + "mydomain.com:80"))
        self.assertTrue(is_link(self.proto + "mydomain.com/index.html"))
        self.assertTrue(is_link(self.proto + "mydomain.com:80/index.html"))
        self.assertTrue(is_link(self.proto + "mydomain.com:80"))
    
    def test_is_not_rel_url_proto_symbols(self):
        self.assertFalse(is_rel(self.proto + "/"))
        self.assertFalse(is_rel(self.proto + "?"))
        self.assertFalse(is_rel(self.proto + "./?"))
        self.assertFalse(is_rel(self.proto + "."))
        self.assertTrue(is_link(self.proto + "/"))
        self.assertTrue(is_link(self.proto + "?"))
        self.assertTrue(is_link(self.proto + "./?"))
        self.assertTrue(is_link(self.proto + "."))

if __name__ == "__main__":
    unittest.main()
