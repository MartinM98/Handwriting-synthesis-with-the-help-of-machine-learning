from skimage.morphology import skeletonize
from skimage import filters
from skimage import io
import matplotlib.pyplot as plt
from skimage.util import invert
import cv2
import numpy as np
import os
from src.file_handler.file_handler import get_file_name
from src.image_processing.common_functions.common_functions import get_dir


def skeletonize_automated():
    """
    Skeletonizes all images with the extension png in the selected directory and
    saves the results.
    Args:
       None
    """
    directory = get_dir()

    for entry in os.scandir(directory):
        if (entry.path.endswith(".png")):
            path2 = get_file_name(entry.path)
            path = entry.path
            image2 = io.imread(path)
            image2 = invert(image2)
            image = image2 > filters.threshold_otsu(image2)

            skeleton = skeletonize(image)
            skeleton = invert(skeleton)

            plt.imsave('/tmp/temp_skel.png', skeleton, cmap=plt.cm.gray)
            image4 = cv2.imread('/tmp/temp_skel.png')
            image4 = cv2.cvtColor(image4, cv2.COLOR_BGR2GRAY)
            for ix, iy in np.ndindex(image4.shape):
                if(image4[ix, iy] != 255):
                    image4[ix, iy] = 0
            _, img = cv2.threshold(image4, 2, 255, cv2.THRESH_BINARY)
            plt.imsave(directory + '/' + path2 + '_skel.png', img, cmap=plt.cm.gray)


if __name__ == '__main__':
    skeletonize_automated()
