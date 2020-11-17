import numpy as np
import cv2
from skimage.filters import gabor
from skimage import img_as_ubyte
from skimage.util import invert
from tkinter import filedialog, Tk
import os


root = Tk()
root.withdraw()
root.directory = filedialog.askdirectory()

directory = root.directory

root.destroy()

thetas = [0.25 * np.pi, 0.75 * np.pi]
lamda = 0.16 * np.pi
for entry in os.scandir(directory):
    if (entry.path.endswith(".png")):
        path2 = os.path.splitext(os.path.split(entry.path)[1])[0]
        path = entry.path
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = np.zeros(shape=img.shape)
        result = img_as_ubyte(result)
        result = invert(result)
        for theta in thetas:
            filt_real, filt_imag = gabor(img, frequency=1 / lamda, theta=theta)
            cv_image = img_as_ubyte(filt_imag)
            cv_image = invert(cv_image)
            result = np.bitwise_and(result, cv_image)
        cv2.imwrite(directory + '/' + path2 + '_control_points.png', result)
