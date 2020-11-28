import numpy as np
import cv2
from skimage import img_as_ubyte
from skimage.util import invert
from tkinter import filedialog, Tk
import os
import sys
import math


def processPart(image, x1, y1, x2, y2):

    points = []
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            point = []
            if image[x, y] == 0:
                point.append(x)
                point.append(y)
                points.append(point)
    return points


def get_dir_and_file():
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(
        ("png files", "*.png"), ("all files", "*.*")))
    directory = os.path.dirname(root.filename)
    path2 = os.path.splitext(os.path.split(root.filename)[1])[0]
    root.destroy()
    return directory, path2, root.filename


def get_image(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(f"Size: {img.shape}")
    return img


def get_dimensions(img, n):
    width = img.shape[0]
    height = img.shape[1]
    x_step = math.ceil(width / n)
    y_step = math.ceil(height / n)
    return width, height, x_step, y_step


def get_box(x, x_step, width, y, y_step, height):
    x1 = x
    x2 = x + x_step - 1
    if x2 >= width:
        x2 = width - 1
    y1 = y
    y2 = y + y_step - 1
    if y2 >= height:
        y2 = height - 1
    return x1, x2, y1, y2


def prepare_blank_image(img):
    img2 = np.zeros(shape=img.shape)
    img2 = img_as_ubyte(img2)
    img2 = invert(img2)
    return img2


def resize_and_show_images(img, img2):
    size = (500, 500)
    img = cv2.resize(img, size)
    img3 = cv2.resize(img2, size)
    cv2.imshow('Original', img)
    cv2.imshow('Limited', img3)
    cv2.waitKey()


def get_parts(img, n, parts):
    width, height, x_step, y_step = get_dimensions(img, n)
    for y in range(0, height, y_step):
        for x in range(0, width, x_step):
            x1, x2, y1, y2 = get_box(x, x_step, width, y, y_step, height)
            parts.append(processPart(img, x1, y1, x2, y2))


def filter_points(img2, parts, n):
    index = 0
    while(n > 0):
        if len(parts[index]) != 0:
            img2[parts[index][0][0], parts[index][0][1]] = 0
            parts[index].pop(0)
            n -= 1
        else:
            min_index = parts.index(max(parts, key=lambda part: len(part)))
            if len(parts[min_index]) == 0:
                break
        index += 1
        index = index % len(parts)


def consecutive():
    if len(sys.argv) == 1:
        exit()
    n = int(sys.argv[1])

    directory, path2, path = get_dir_and_file()

    img = get_image(path)

    parts = []
    get_parts(img, n, parts)

    if len(sys.argv) == 2:
        exit()

    n = int(sys.argv[2])
    img2 = prepare_blank_image(img)
    filter_points(img2, parts, n)
    resize_and_show_images(img, img2)
    cv2.imwrite(directory + '/' + path2 + '_filtered.png', img2)


if __name__ == '__main__':
    consecutive()
