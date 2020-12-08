from skimage.morphology import skeletonize
from skimage import filters
from skimage.util import invert
import cv2
import numpy as np


def skeletonize_image(image: np.ndarray = None, path: str = None):
    """
    Skeletonizes the image.

    Args:
       image (np.ndarray, optional): the image that should be processed.
       path (str, optional): the path to the image that should
       be processed.

    Returns:
        (np.ndarray): The skeletonized image.
    """
    if image is None:
        image = cv2.imread(path)

    image = invert(image)
    image = image > filters.threshold_otsu(image)

    skeleton = skeletonize(image)
    skeleton = invert(skeleton)

<<<<<<< HEAD
    image = cv2.cvtColor(skeleton, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
=======
    plt.imsave('./tmp/temp_skel.png', skeleton, cmap=plt.cm.gray)
    image4 = cv2.imread('./tmp/temp_skel.png')
    image4 = cv2.cvtColor(image4, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(image4, 2, 160, cv2.THRESH_BINARY)
    for ix, iy in np.ndindex(image4.shape):
        if(image4[ix, iy] != 255):
            image4[ix, iy] = 0
>>>>>>> 6c893aa9bbc3b80d4999b8e46aa2818e4113da44

    return image
