from scrapy.http import HtmlResponse

import os
import sys
import unittest


# For Python 2.x compatibility, unless we install
# this whole spider directory as a package, Python
# does not know where to look for "logospider"
logoDir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "logofinder"))
sys.path.insert(0, logoDir)

import logospider  # noqa


class TestLogoSpider(unittest.TestCase):

    ENCODING = "utf-8"
    SITEDIR = "websites/"
    START_URL = "start_url"

    def setUp(self):
        self.spider = logospider.LogoSpider(self.START_URL)

    def test_invalid_init(self):
        # start_url cannot be "None"
        self.assertRaises(ValueError, logospider.LogoSpider, None)

    def test_empty_website(self):
        body_file = open(self.SITEDIR + "empty.html", "r")
        body = body_file.read()
        body_file.close()

        response = HtmlResponse(body=body, url=self.START_URL,
                                encoding=self.ENCODING)
        self.spider.parse(response)
        self.assertDictEqual(self.spider.images, {})

    def test_invalid_urls(self):
        body_file = open(self.SITEDIR + "invalid_urls.html", "r")
        body = body_file.read()
        body_file.close()

        response = HtmlResponse(body=body, url=self.START_URL,
                                encoding=self.ENCODING)
        self.spider.parse(response)
        self.assertDictEqual(self.spider.images, {})

    def test_multi_empty(self):
        body_file = open(self.SITEDIR + "multipage_one.html", "r")
        body = body_file.read()
        body_file.close()

        response = HtmlResponse(body=body, url=self.START_URL,
                                encoding=self.ENCODING)
        self.spider.parse(response)
        self.assertDictEqual(self.spider.images, {})


if __name__ == '__main__':
    unittest.main()
