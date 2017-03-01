"""
Helper file used for classifying images retrieved from a website.

Largely adapted from Google's Tensorflow model's repository, which can be
found at the following link:

https://github.com/tensorflow/models
"""

from __future__ import print_function
from PIL import Image

import tensorflow as tf
import numpy as np
import os.path
import re

# For Python 2.x compatibility, BytesIO does
# not exist, and its closest equivalent is the
# StringIO class from the StringIO module.
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


class NodeLookup(object):

    LABEL_MAP_PROTO = "imagenet_2012_challenge_label_map_proto.pbtxt"
    LABEL_MAP = "imagenet_synset_to_human_label_map.txt"

    def __init__(self, model_dir):
        """
        Initialize a NodeLookup instance.

        :param model_dir: The directory for all of the models used for
                          training our classifier.
        """

        self.model_dir = model_dir
        self.node_lookup = self.load_lookup()

    def load_lookup(self):
        """
        Loads a human readable English name for each softmax node.

        :return: dictionary from integer node ID to human-readable string.
        """

        label_lookup_path = os.path.join(self.model_dir, self.LABEL_MAP_PROTO)
        uid_lookup_path = os.path.join(self.model_dir, self.LABEL_MAP)

        if not tf.gfile.Exists(uid_lookup_path):
            tf.logging.fatal("File does not exist %s", uid_lookup_path)
        if not tf.gfile.Exists(label_lookup_path):
            tf.logging.fatal("File does not exist %s", label_lookup_path)

        # Loads mapping from string UID to human-readable string.
        proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
        p = re.compile(r"[n\d]*[ \S,]*")
        uid_to_human = {}

        for line in proto_as_ascii_lines:
            parsed_items = p.findall(line)
            uid = parsed_items[0]

            human_string = parsed_items[2]
            uid_to_human[uid] = human_string

        # Loads mapping from string UID to integer node ID.
        proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
        node_id_to_uid = {}

        for line in proto_as_ascii:
            if line.startswith("  target_class:"):
                target_class = int(line.split(": ")[1])

            if line.startswith("  target_class_string:"):
                target_class_string = line.split(": ")[1]
                node_id_to_uid[target_class] = target_class_string[1:-2]

        # Loads the final mapping of integer node ID to human-readable string.
        node_id_to_name = {}

        for key, val in node_id_to_uid.items():
            if val not in uid_to_human:
                tf.logging.fatal("Failed to locate: %s", val)

            name = uid_to_human[val]
            node_id_to_name[key] = name

        return node_id_to_name

    def id_to_string(self, node_id):
        """
        Convert node ID to human-readable string.

        :param node_id: The node ID whose human-readable string we want.
        :return: The human-readable string associated with this node ID.
        """

        if node_id not in self.node_lookup:
            return ""

        return self.node_lookup[node_id]


class ImageClassifier(object):

    GRAPH_DEF = "classify_image_graph_def.pb"

    def __init__(self, model_dir):
        """
        Initialize an ImageClassifier instance.

        :param model_dir: The directory for all of the models used for
                          training our classifier.
        """

        self.model_dir = model_dir

    def create_graph(self):
        """
        Creates a graph from saved GraphDef file and returns a saver.
        """

        saved_graph_def = os.path.join(self.model_dir, self.GRAPH_DEF)
        with tf.gfile.FastGFile(saved_graph_def, "rb") as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name="")

    def classify(self, image_data):
        """
        Classify provided image data.

        :param image_data: Image data that we are to classify. Images that we
                           classify is expected to be encoded (or compressed)
                           in a format like JPEG, PNG, or GIF.
        :return A tuple of the classification and confidence level of
                the top prediction from the classifier.
        """

        self.create_graph()

        with tf.Session() as sess:
            image = Image.open(BytesIO(image_data))
            image_data = image.convert("RGB")

            softmax_tensor = sess.graph.get_tensor_by_name("softmax:0")
            predictions = sess.run(softmax_tensor,
                                   {"DecodeJpeg:0": image_data})
            predictions = np.squeeze(predictions)

            # Creates node ID --> English string lookup.
            node_lookup = NodeLookup(self.model_dir)

            # We just want the top prediction.
            node_id = predictions.argsort()[-1]

            human_string = node_lookup.id_to_string(node_id)
            score = predictions[node_id]

            return human_string, score
