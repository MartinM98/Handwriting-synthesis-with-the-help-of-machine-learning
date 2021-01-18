from skimage.morphology import skeletonize
from skimage import filters
from skimage.util import invert
import cv2
import numpy as np
import warnings


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

    if image is None:
        raise Exception("Empty image path: " + path)

    image = invert(image)
    warnings.filterwarnings("ignore")
    try:
        image = image > filters.threshold_otsu(image)

        skeleton = skeletonize(image)
        skeleton = invert(skeleton)

        image = cv2.cvtColor(skeleton, cv2.COLOR_BGR2GRAY)
        _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    except ValueError:
        print('Skeletonization warning')

    return image
