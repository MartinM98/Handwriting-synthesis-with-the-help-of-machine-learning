from skimage.morphology import skeletonize
from skimage import filters
from skimage import io
import matplotlib.pyplot as plt
from skimage.util import invert
import cv2
import numpy as np
import os
import sys


def skeletonize_function(directory: str):
    """
    Applies the skeletonization to all images with the extension
    png in the directory given as parameter to the script.
    Args:
       directory (str): path to the directory that should be processed (Optional).
    """
    if directory is None:
        directory = sys.argv[1]

    for entry in os.scandir(directory):
        if (entry.path.endswith(".png")):
            path2 = os.path.splitext(os.path.split(entry.path)[1])[0]
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
            plt.imsave(directory + '/skel/' + path2 + '_skel.png', img, cmap=plt.cm.gray)


if __name__ == '__main__':
    skeletonize_function(None)
