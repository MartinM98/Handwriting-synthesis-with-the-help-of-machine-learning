from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from src.image_processing.resize import crop_image
import numpy as np
import json
import base64
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf1  # noqa: E402
tf = tf1.compat.v1
tf.disable_v2_behavior()


def process_file(model_path: str, input_path: str, output_path: str, use_gpu: bool = False):
    """
    Generates a letter from skeleton based on given model

    Args:
        model_path (str): Path to model
        input_path (str): Path to skeleton
        output_path (str): Path to output
        use_gpu (bool): Flag whether to use GPU or not
    """
    with open(input_path, "rb") as f:
        input_data = f.read()

    input_instance = dict(input=base64.urlsafe_b64encode(
        input_data).decode("ascii"), key="0")
    input_instance = json.loads(json.dumps(input_instance))

    if use_gpu:
        config = tf.ConfigProto()
    else:
        config = tf.ConfigProto(device_count={'GPU': 0})

    with tf.Session(config=config) as sess:
        saver = tf.train.import_meta_graph(model_path + "/export.meta")
        saver.restore(sess, model_path + "/export")
        input_vars = json.loads(tf.get_collection("inputs")[0])
        output_vars = json.loads(tf.get_collection("outputs")[0])
        input = tf.get_default_graph().get_tensor_by_name(input_vars["input"])
        output = tf.get_default_graph().get_tensor_by_name(
            output_vars["output"])
        input_value = np.array(input_instance["input"])
        output_value = sess.run(
            output, feed_dict={input: np.expand_dims(input_value, axis=0)})[0]

    output_instance = dict(output=output_value.decode("ascii"), key="0")

    b64data = output_instance["output"]
    b64data += "=" * (-len(b64data) % 4)
    output_data = base64.urlsafe_b64decode(b64data.encode("ascii"))

    with open(output_path, "wb") as f:
        f.write(output_data)


def process_directory(model_path: str, input_path: str, use_gpu: bool = False):
    """
    Generates letters from skeletons based on given model in the same directory but different subfolder

    Args:
        model_path (str): Path to model
        input_path (str): Path to skeleton
        use_gpu (bool): Flag whether to use GPU or not
    """
    if use_gpu:
        config = tf.ConfigProto()
    else:
        config = tf.ConfigProto(device_count={'GPU': 0})

    with tf.Session(config=config) as sess:
        saver = tf.train.import_meta_graph(model_path + "/export.meta")
        saver.restore(sess, model_path + "/export")
        input_vars = json.loads(tf.get_collection("inputs")[0])
        output_vars = json.loads(tf.get_collection("outputs")[0])
        input = tf.get_default_graph().get_tensor_by_name(input_vars["input"])
        output = tf.get_default_graph().get_tensor_by_name(
            output_vars["output"])

        for path, subdirs, files in os.walk(input_path):
            for name in files:
                if name.endswith('.png'):
                    output_path = path.replace('skeletons', 'synthesized')
                    if not os.path.exists(output_path):
                        os.mkdir(output_path)

                    with open(os.path.join(path, name), "rb") as f:
                        input_data = f.read()

                    input_instance = dict(input=base64.urlsafe_b64encode(
                        input_data).decode("ascii"), key="0")
                    input_instance = json.loads(json.dumps(input_instance))
                    input_value = np.array(input_instance["input"])
                    output_value = sess.run(
                        output, feed_dict={input: np.expand_dims(input_value, axis=0)})[0]
                    output_instance = dict(
                        output=output_value.decode("ascii"), key="0")
                    b64data = output_instance["output"]
                    b64data += "=" * (-len(b64data) % 4)
                    output_data = base64.urlsafe_b64decode(b64data.encode("ascii"))
                    with open(os.path.join(output_path, name), "wb") as f:
                        f.write(output_data)
                    crop_image(os.path.join(output_path, name), os.path.join(output_path, name))
    tf.reset_default_graph()


# process_directory('../graphical_interface/export', '../graphical_interface/synthesis/skeletons')
