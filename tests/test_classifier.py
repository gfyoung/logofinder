import os
import sys
import nose
import logging
import unittest

# We don't want Tensorflow output filling up our test output
# unless it is some major error that we should be aware of.
logging.getLogger("tensorflow").setLevel(logging.WARNING)

# For Python 2.x compatibility, unless we install
# this whole spider directory as a package, Python
# does not know where to look for "logospider"
logoDir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "logofinder"))
sys.path.insert(0, logoDir)

try:
    import classifier  # noqa
except ImportError as e:
    # Travis has issues running Tensorflow due to
    # .so file incompatibilities, but that shouldn't
    # stop us from testing locally if possible.
    raise nose.SkipTest("Import failed: " + str(e))


class TestLogoSpider(unittest.TestCase):

    MODEL_DIR = "models"

    def setUp(self):
        self.classifier = classifier.ImageClassifier(self.MODEL_DIR)

    def test_invalid_encoding(self):
        # Encoding must either be GIF, JPG, or PNG.
        self.assertRaises(ValueError, self.classifier.classify,
                          "image_data", "invalid_encoding")


if __name__ == '__main__':
    unittest.main()
