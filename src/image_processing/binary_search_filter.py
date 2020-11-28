import numpy as np
import cv2
from skimage import img_as_ubyte
from skimage.util import invert
from tkinter import filedialog, Tk
import os
import sys
import math
import random


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


def get_dimensions(img, n):
    width = img.shape[0]
    height = img.shape[1]
    x_step = math.ceil(width / n)
    y_step = math.ceil(height / n)
    return width, height, x_step, y_step


def get_image(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(f"Size: {img.shape}")
    return img


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


def add_end_points(halves, img2, parts2):
    halves.append(0)
    rand_index = random.randint(0, len(parts2[0]) - 1)
    img2[parts2[0][rand_index][0], parts2[0][rand_index][1]] = 0
    parts2[0].pop(rand_index)
    halves.append(len(parts2) - 1)
    rand_index = random.randint(0, len(parts2[len(parts2) - 1]) - 1)
    img2[parts2[len(parts2) - 1][rand_index][0],
         parts2[len(parts2) - 1][rand_index][1]] = 0
    parts2[len(parts2) - 1].pop(rand_index)


def add_point(img2, tmp, halves, i, parts2, offset):
    mid = math.floor((halves[i + 1] - halves[i]) / 2)
    tmp.insert(i + 1 + offset, halves[i] + mid)
    rand_index = random.randint(
        0, len(parts2[halves[i] + mid]) - 1)
    img2[parts2[halves[i] + mid][rand_index][0],
         parts2[halves[i] + mid][rand_index][1]] = 0
    parts2[halves[i] + mid].pop(rand_index)


def binary_search_filter():
    if len(sys.argv) == 1:
        exit()
    n = int(sys.argv[1])

    directory, path2, path = get_dir_and_file()

    img = get_image(path)

    width, height, x_step, y_step = get_dimensions(img, n)

    parts = []
    i = 1
    for y in range(0, height, y_step):
        for x in range(0, width, x_step):
            x1, x2, y1, y2 = get_box(x, x_step, width, y, y_step, height)
            parts.append(processPart(img, x1, y1, x2, y2))
            i += 1

    if len(sys.argv) == 2:
        exit()

    n = int(sys.argv[2])

    img2 = prepare_blank_image(img)

    parts2 = [part for part in parts if len(part) > 0]
    state = 2
    while(state < n):
        parts2 = [part for part in parts2 if len(part) > 0]
        halves = []
        add_end_points(halves, img2, parts2)
        while(len(halves) < n and len(halves) < len(parts2)):
            tmp = halves.copy()
            offset = 0
            for i in range(0, len(halves) - 1):
                if halves[i] == (halves[i + 1] - 1):
                    continue
                add_point(img2, tmp, halves, i, parts2, offset)
                offset += 1
                state += 1
                if(state == n):
                    break
            halves = tmp
            if(state == n):
                break

    resize_and_show_images(img, img2)
    cv2.imwrite(directory + '/' + path2 + '_filtered.png', img2)


if __name__ == '__main__':
    binary_search_filter()
