import logospider
import unittest


class TestLogoSpider(unittest.TestCase):

    def test_invalid_init(self):
        # start_url cannot be "None"
        self.assertRaises(ValueError, logospider.LogoSpider, None)


if __name__ == '__main__':
    unittest.main()
