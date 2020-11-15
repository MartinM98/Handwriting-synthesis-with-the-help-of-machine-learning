import numpy as np
from src.synthesis.bspline import draw_bspline
import cv2


def control_points(path_to_image: str):
    """#TODO

    Args:
        path_to_image (str): [description]

    Returns:
        [type]: [description]
    """
    img = cv2.imread(path_to_image)
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    contours = sorted(contours, key=lambda x: cv2.contourArea(x))[:-1]
    result = list()
    for cnt in contours:
        # compute the center of the contour
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        result.append((cX, cY))
    return result


if __name__ == '__main__':
    points = control_points(
        'C:\\Users\\Patryk\\Downloads\\B_control_points.png')
    print(points)
    draw_bspline(np.array(points))
