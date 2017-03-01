import os
import sys
import nose
import unittest

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

    def setUp(self):
        directory = os.path.dirname(__file__)

        self.MODEL_DIR = os.path.join(directory, "..", "logofinder", "models")
        self.classifier = classifier.ImageClassifier(self.MODEL_DIR)

        self.IMAGE_DIR = os.path.join(directory, "images")

    def test_jpeg(self):
        filename = os.path.join(self.IMAGE_DIR, "panda.jpg")
        image_data = open(filename, "rb").read()

        human_string, score = self.classifier.classify(image_data)
        self.assertIn("panda", human_string,
                      "Classifier should have seen a panda")

        confidence = 0.85
        msg = "Confidence should be at least {pct}".format(pct=confidence)

        self.assertGreaterEqual(score, confidence, msg)

    def test_png(self):
        filename = os.path.join(self.IMAGE_DIR, "panda.png")
        image_data = open(filename, "rb").read()

        human_string, score = self.classifier.classify(image_data)
        self.assertIn("panda", human_string,
                      "Classifier should have seen a panda")

        confidence = 0.85
        msg = "Confidence should be at least {pct}".format(pct=confidence)

        self.assertGreaterEqual(score, confidence, msg)

    def test_gif(self):
        filename = os.path.join(self.IMAGE_DIR, "panda.gif")
        image_data = open(filename, "rb").read()

        human_string, score = self.classifier.classify(image_data)
        self.assertIn("panda", human_string,
                      "Classifier should have seen a panda")

        confidence = 0.85
        msg = "Confidence should be at least {pct}".format(pct=confidence)

        self.assertGreaterEqual(score, confidence, msg)

    def test_minivan(self):
        filename = os.path.join(self.IMAGE_DIR, "minivan.jpg")
        image_data = open(filename, "rb").read()

        human_string, score = self.classifier.classify(image_data)
        self.assertIn("minivan", human_string,
                      "Classifier should have seen a minivan")

        confidence = 0.65
        msg = "Confidence should be at least {pct}".format(pct=confidence)

        self.assertGreaterEqual(score, confidence, msg)

    def test_human_suit(self):
        filename = os.path.join(self.IMAGE_DIR, "human-suit.jpg")
        image_data = open(filename, "rb").read()

        human_string, score = self.classifier.classify(image_data)
        self.assertIn("suit", human_string,
                      "Classifier should have seen a suit")

        confidence = 0.50
        msg = "Confidence should be at least {pct}".format(pct=confidence)

        self.assertGreaterEqual(score, confidence, msg)

    def test_dog_painting(self):
        filename = os.path.join(self.IMAGE_DIR, "dog-painting.jpg")
        image_data = open(filename, "rb").read()

        human_string, score = self.classifier.classify(image_data)
        self.assertIn("Rhodesian ridgeback", human_string,
                      "Classifier should have seen a Rhodesian ridgeback")

        confidence = 0.30
        msg = "Confidence should be at least {pct}".format(pct=confidence)

        self.assertGreaterEqual(score, confidence, msg)


if __name__ == '__main__':
    unittest.main()
