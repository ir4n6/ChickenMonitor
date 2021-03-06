import tensorflow as tf
import re
import numpy as np
import sys
import os

label_lookup_path = "imagenet/imagenet_2012_challenge_label_map_proto.pbtxt"
uid_lookup_path = "imagenet/imagenet_synset_to_human_label_map.txt"
num_predictions = 3

class ImageNet(object):
    def __init__(self):
        self.node_lookup = self.load_imagenet(label_lookup_path, uid_lookup_path)

    def load_imagenet(self, label_lookup_path, uid_lookup_path):
        """Loads human readable name for each softmax node"""
        # Loads mapping from string UID to human-readable string
        proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
        uid_to_human = {}
        p = re.compile(r'[n\d]*[ \S,]*')
        for line in proto_as_ascii_lines:
            parsed_items = p.findall(line)
            uid = parsed_items[0]
            human_string = parsed_items[2]
            uid_to_human[uid] = human_string

        # Loads mapping from string UID to integer node ID.
        node_id_to_uid = {}
        proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
        for line in proto_as_ascii:
            if line.startswith('  target_class:'):
                target_class = int(line.split(': ')[1])
            if line.startswith('  target_class_string:'):
                target_class_string = line.split(': ')[1]
                node_id_to_uid[target_class] = target_class_string[1:-2]

        # Loads the final mapping of integer node ID to human-readable string
        node_id_to_name = {}
        for key, val in node_id_to_uid.items():
            if val not in uid_to_human:
                tf.logging.fatal('Failed to locate: {}'.format(val))
            name = uid_to_human[val]
            node_id_to_name[key] = name

        return node_id_to_name

    def id_to_string(self, node_id):
        if node_id not in self.node_lookup:
            return ''
        return self.node_lookup[node_id]

    def create_graph(self):
        with tf.gfile.FastGFile("imagenet/classify_image_graph_def.pb", 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name='')

    def run_inference_on_image(self, image):
        if not tf.gfile.Exists(image):
            tf.logging.fatal('File does not exist %s', image)
        image_data = tf.gfile.FastGFile(image, 'rb').read()

        self.create_graph()

        with tf.Session() as sess:
            softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
            self.predictions = np.squeeze(predictions)

            # Creates node ID --> English string lookup.
            #node_lookup = ImageNet()

            top_k = self.predictions.argsort()[-num_predictions:][::-1]
            for node_id in top_k:
                human_string = self.id_to_string(node_id)
                score = self.predictions[node_id]
                print("%s (score = %.5f)" % (human_string, score))
            print()

if __name__ == '__main__':
    # This currently will just go over an entire directory - need to make it a bit more flexible
    if len(sys.argv > 1):
        image_dir = sys.argv[1]
    else:
        image_dir = "images"
    _dir = os.listdir(image_dir)
    for image in _dir:
        imageNet = ImageNet()
        print("Filename: {}".format(image))
        imageNet.run_inference_on_image("{}/{}".format(image_dir, image))
