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

    def test_invalid_init(self):
        # start_url cannot be "None"
        self.assertRaises(ValueError, logospider.LogoSpider, None)


if __name__ == '__main__':
    unittest.main()
