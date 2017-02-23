#!/usr/bin/env python

"""
Script used for extracting a website logo from a website.
To use this script, run the following command:

scrapy runspider logospider.py -a start_url=<start_url>
"""

import scrapy


class LogoSpider(scrapy.Spider):
    name = "logospider"

    def __init__(self, start_url, *args, **kwargs):
        """
        Initialize a LogoSpider instance.

        :param start_url: URL at which to start scraping.
        :raises ValueError: Null start_url provided.
        """
        super(LogoSpider, self).__init__(*args, **kwargs)

        if start_url is None:
            raise ValueError("Starting URL cannot be None")

        self.start_url = start_url

    def start_requests(self):
        """
        Begin scraping the website designated by `self.start_url`.
        """
        yield(scrapy.Request(self.start_url, callback=self.parse))

    def parse(self, response):
        """
        Parse the response returned from making a request to a URL.

        :param response: The website response to parse.
        """
        pass
