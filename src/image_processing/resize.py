import cv2
import numpy as np
import os


def resize_image(image_path: str, width: int, height: int):
    """
    Resizes image from given path to given size by pasting it into center of white baackground of given size

    Args:
        image_path (str): Path to image
        width (int): Width in pixels
        height (int): Height in pixels

    Returns:
        (array): Resized image
    """
    resized = np.zeros([width, height, 3], dtype=np.uint8)
    resized.fill(255)

    image = cv2.imread(image_path)
    (h, w) = image.shape[:2]

    yoff = round((height - h) / 2)
    xoff = round((width - w) / 2)

    resized[yoff:yoff + h, xoff:xoff + w] = image

    return resized


def resize_directory(input_path: str, output_path: str):
    """
    Resizes all files in given directory to given outputt directory

    Args:
        input_path (str): Input directory
        output_path (str): Output directory
    """
    i = 0
    for path, subdirs, files in os.walk(input_path):
        for name in files:
            resized = resize_image(os.path.join(path, name), 256, 256)
            cv2.imwrite(os.path.join(output_path, str(i) + '.png'), resized)
            i += 1
