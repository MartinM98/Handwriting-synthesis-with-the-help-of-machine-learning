import cv2
import numpy as np


def preproduce(file_path: str):
    image = cv2.imread(file_path, cv2.COLOR_BGR2GRAY)
    height, width = image.shape

    cv2.imshow('Image', image)
    cv2.waitKey()

    # finding contur of the biggest area
    ret, thresh = cv2.threshold(image, 127, 255, 0)

    if (int(cv2.__version__[0]) > 3):
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        im2, contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = sorted(contours, key=cv2.contourArea, reverse=True)[:3]

    if len(contours) != 0:
        # draw in blue the contours that were founded
        cv2.drawContours(image, contours, -1, 255, 3)

        # find the biggest countour (c) by the area
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        # draw the biggest contour (c) in green
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    path = '/home/patryk/Pulpit/Handwriting-synthesis-with-the-help-of-machine-learning/data/a01-000u.png'
    preproduce(path)
