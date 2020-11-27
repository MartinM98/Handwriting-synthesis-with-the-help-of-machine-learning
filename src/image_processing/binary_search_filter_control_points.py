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
                point.append(x)
                point.append(y)
                points.append(point)
    return points


def binary_search_filter():
    if len(sys.argv) == 1:
        exit()

    n = int(sys.argv[1])
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir="/Users/martinmrugala/Desktop/GP_III",
                                               title="Select file", filetypes=(("png files", "*.png"), ("all files", "*.*")))
    directory = os.path.dirname(root.filename)
    path2 = os.path.splitext(os.path.split(root.filename)[1])[0]
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

            parts.append(processPart(img, x1, y1, x2, y2))
            i += 1

    if len(sys.argv) == 2:
        exit()

    n = int(sys.argv[2])
    img2 = np.zeros(shape=img.shape)
    img2 = img_as_ubyte(img2)
    img2 = invert(img2)

    parts2 = [part for part in parts if len(part) > 0]

    state = 2
    while(state < n):
        parts2 = [part for part in parts2 if len(part) > 0]
        halves = []
        halves.append(0)
        rand_index = random.randint(0, len(parts2[0]) - 1)
        img2[parts2[0][rand_index][0], parts2[0][rand_index][1]] = 0
        parts2[0].pop(rand_index)
        halves.append(len(parts2) - 1)
        rand_index = random.randint(0, len(parts2[len(parts2) - 1]) - 1)
        img2[parts2[len(parts2) - 1][rand_index][0],
             parts2[len(parts2) - 1][rand_index][1]] = 0
        parts2[len(parts2) - 1].pop(rand_index)
        while(len(halves) < n and len(halves) < len(parts2)):
            tmp = halves.copy()
            offset = 0
            for i in range(0, len(halves) - 1):
                if halves[i] == (halves[i + 1] - 1):
                    continue
                mid = math.floor((halves[i + 1] - halves[i]) / 2)
                tmp.insert(i + 1 + offset, halves[i] + mid)
                rand_index = random.randint(
                    0, len(parts2[halves[i] + mid]) - 1)
                img2[parts2[halves[i] + mid][rand_index][0],
                     parts2[halves[i] + mid][rand_index][1]] = 0
                parts2[halves[i] + mid].pop(rand_index)
                offset += 1
                state += 1
                if(state == n):
                    break
            halves = tmp
            if(state == n):
                break

    size = (500, 500)
    img = cv2.resize(img, size)
    img3 = cv2.resize(img2, size)
    cv2.imshow('Original', img)
    cv2.imshow('Limited', img3)

    cv2.waitKey()

    cv2.imwrite(directory + '/' + path2 + '_filtered.png', img2)


if __name__ == '__main__':
    binary_search_filter()
