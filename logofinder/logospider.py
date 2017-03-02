"""
Script used for extracting a website logo from a website.
To use this script, run the following command:

scrapy runspider logospider.py -a start_url=<start_url>

If you would like to restrict the logging output from scrapy
when running this script you can write the command as follows:

scrapy runspider logospider.py --loglevel=WARNING -a start_url=<start_url>
"""

from scrapy.selector import Selector

import scrapy
import classifier


class LogoSpider(scrapy.Spider):
    name = "logospider"
    model_dir = "models"

    # Link prefixes that would render it invalid
    # for further parsing or following.
    invalid_prefixes = ["tel", "http", "maito", "mailto", "javascript"]

    def __init__(self, start_url, *args, **kwargs):
        """
        Initialize a LogoSpider instance.

        :param start_url: URL at which to start scraping.
        :raises ValueError: Null start_url provided.
        """
        super(LogoSpider, self).__init__(*args, **kwargs)

        if start_url is None:
            raise ValueError("Starting URL cannot be None")

        self.images = {}
        self.start_url = start_url
        self.classifier = classifier.ImageClassifier(self.model_dir)

    def start_requests(self):
        """
        Begin scraping the website designated by `self.start_url`.
        """
        yield(scrapy.Request(self.start_url, callback=self.parse))

    def valid_link(self, link):
        """
        Check whether a link is valid for continual parsing or requesting.

        :param link: The link to check for validity.
        :return Whether the link is valid or not.
        """
        for prefix in self.invalid_prefixes:
            if link.startswith(prefix):
                return False

        return True

    def parse(self, response):
        """
        Parse the response returned from making a request to a URL.

        :param response: The website response to parse.
        """
        selector = Selector(response).xpath("//body")

        for node in selector:
            for src in node.xpath("//img/@src").extract():
                if self.valid_link(src):
                    src = response.urljoin(src)
                    yield scrapy.Request(src, callback=self.store_img)

            for href in node.xpath("//a/@href").extract():
                if self.valid_link(href):
                    href = response.urljoin(href)
                    yield scrapy.Request(href, callback=self.parse)

    def store_img(self, response):
        """
        Store the returned image for future processing by our classifier.

        :param response: The website response containing the image.
        """

        # From an organizational perspective, it seems more logical to
        # decouple the actual image processing from the scraping. On the
        # other hand, it means we have to store these images in memory,
        # which could be costly if the images were large enough.
        #
        # For the ground truth data provided, the images did not consume
        # too much memory. Thus, this implementation was passable for this
        # set of data, but in the future, it would be better to somehow
        # pass along the image data through some pipeline and have another
        # worker handle the image processing and classification.
        self.images[response.url] = response.body

    def close(self, reason):
        """
        Method called when the spider finishes scraping the website.

        Regardless of whether the spider closed out of error or completed
        successfully, we use whatever images we have found and determine
        whether any of them could be logos.

        :param reason: The reason that the spider completed.
        :return: The link corresponding to the logo image, or None.
        """

        if not self.images.items():
            return None

        for link, img in self.images.items():
            # Ultimately, we would want to combine image classifications
            # with keywords in the website (e.g. searching the meta tags)
            # and then find their similarities with the classifications
            # made on these images to help determine which image is the
            # website logo or not.
            label, score = self.classifier.classify(img)
            yield {"label": label, "score": score, "link": link}
