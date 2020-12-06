import cv2
import numpy as np
import os


def resize_image(image_path, width, height):
    resized = np.zeros([width, height, 3], dtype=np.uint8)
    resized.fill(255)

    image = cv2.imread(image_path)
    (h, w) = image.shape[:2]

    yoff = round((height - h) / 2)
    xoff = round((width - w) / 2)

    resized[yoff:yoff + h, xoff:xoff + w] = image

    return resized


def resize_directory(input_path, output_path):
    i = 0
    for path, subdirs, files in os.walk(input_path):
        for name in files:
            resized = resize_image(os.path.join(path, name), 256, 256)
            cv2.imwrite(os.path.join(output_path, str(i) + '.png'), resized)
            i += 1
