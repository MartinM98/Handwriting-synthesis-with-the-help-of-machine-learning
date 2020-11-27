import numpy as np
import cv2
from skimage import img_as_ubyte
from skimage.util import invert
from tkinter import filedialog, Tk
import os
import sys
from PIL import Image
import math
import random


def PILcv2(image):
    return Image.fromarray(image)


def cv2PIL(image):
    return np.asarray(image)


def processPart(image, x1, y1, x2, y2):
    points = []
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            point = []
            if image[x, y] == 0:
                print(image[x, y])
                point.append(x)
                point.append(y)
                points.append(point)
    return points


def random_filter():
    if len(sys.argv) == 1:
        exit()

    n = int(sys.argv[1])
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir="/Users/martinmrugala/Desktop/GP_III",
                                               title="Select file", filetypes=(("png files", "*.png"), ("all files", "*.*")))
    path2 = os.path.splitext(os.path.split(root.filename)[1])[0]
    directory = os.path.dirname(root.filename)
    root.destroy()

    img = cv2.imread(root.filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(f"Size: {img.shape}")

    width = img.shape[0]
    height = img.shape[1]
    parts = []
    x_step = math.ceil(width / n)
    y_step = math.ceil(height / n)
    i = 1
    for y in range(0, height, y_step):
        for x in range(0, width, x_step):
            x1 = x
            x2 = x + x_step - 1
            if x2 >= width:
                x2 = width - 1
            y1 = y
            y2 = y + y_step - 1
            if y2 >= height:
                y2 = height - 1

            print(
                f"Square {i}:\n[{x1},{y1}]\t[{x2},{y1}]\n[{x1},{y2}]\t[{x2},{y2}]\n\n")
            parts.append(processPart(img, x1, y1, x2, y2))
            i += 1
    i2 = 1
    for part in parts:
        print(f"Part: {i2}")
        i2 += 1
        for point in part:
            print(f"Point: [{point[0]},{point[1]}]")

    if len(sys.argv) == 2:
        exit()

    n = int(sys.argv[2])
    img2 = np.zeros(shape=img.shape)
    img2 = img_as_ubyte(img2)
    img2 = invert(img2)

    checked = np.zeros(sum(len(part) > 0 for part in parts))
    n_checked = 0
    index = random.randint(0, len(checked) - 1 - n_checked)
    parts2 = [part for part in parts if len(part) > 0]

    while(n > 0):
        print(index)
        if len(parts2[index]) != 0:
            rand_index = random.randint(0, len(parts2[index]) - 1)
            img2[parts2[index][rand_index][0],
                 parts2[index][rand_index][1]] = 0
            parts2[index].pop(rand_index)
            n -= 1
        else:
            min_index = parts.index(max(parts, key=lambda part: len(part)))
            if len(parts[min_index]) == 0:
                break
        checked[index] = 1
        n_checked += 1
        if n_checked == len(checked):
            checked = np.zeros(len(checked))
        n_checked = n_checked % len(checked)
        index = random.randint(0, len(checked) - 1 - n_checked)
        i = 0
        temp = 0
        while(checked[temp] == 1):
            temp += 1
        while(i < index):
            if checked[temp] == 0:
                i += 1
            temp += 1
        index = temp

    size = (500, 500)
    img = cv2.resize(img, size)
    img3 = cv2.resize(img2, size)
    cv2.imshow('Original', img)
    cv2.imshow('Limited', img3)

    cv2.waitKey()

    cv2.imwrite(directory + '/' + path2 + '_filtered.png', img2)


if __name__ == '__main__':
    random_filter()
