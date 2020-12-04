from skimage.morphology import skeletonize
from skimage import filters
from skimage import io
import matplotlib.pyplot as plt
from skimage.util import invert
import cv2
import numpy as np


def skeletonize_image(image2: np.ndarray = None, path: str = None):
    """
    Skeletonizes the image.

    Args:
       image2 (np.ndarray, optional): the image that should be processed.
       path (str, optional): the path to the image that should
       be processed.

    Returns:
        (np.ndarray): The skeletonized image.
    """
    if image2 is None:
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

    return image4
