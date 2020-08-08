""" Threshold for database images """
import os
import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image

def nothing():
    """ Empty function for createTrackbar """

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir='./', title='Select file', \
        filetypes=[('png files', '.png')])
    if root.filename == '':
        print('No file has been selected')
        exit()
    path, file = os.path.split(root.filename)

    # Create a black image, a window
    img = cv2.imread(root.filename, 0)
    img2 = cv2.imread(root.filename, 0)
    cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)

    # create trackbar for threshold range
    cv2.createTrackbar('T', 'image', 0, 255, nothing)

    # create switch for ON/OFF functionality
    SWITCH = '0 : OFF \n1 : ON'
    cv2.createTrackbar(SWITCH, 'image', 0, 1, nothing)
    cv2.createTrackbar('SAVE', 'image', 0, 1, nothing)

    while 1:
        cv2.imshow('image', img2)
        k = cv2.waitKey(5)
        if k == 97:
            break

        # get current positions of four trackbars
        t = cv2.getTrackbarPos('T', 'image')
        s = cv2.getTrackbarPos(SWITCH, 'image')
        s2 = cv2.getTrackbarPos('SAVE', 'image')

        if s == 0:
            img2 = img
        else:
            ret, img2 = cv2.threshold(img, t, 255, cv2.THRESH_BINARY)
        if s2 == 1:
            name = file[:-4] + '_new.png'
            cv2.imwrite(path + '/' + name, img2)

    cv2.destroyAllWindows()
    im = Image.open(path + '/' + name)
    width, height = im.size

    command = 'tesseract ' + path + '/' + name + ' ' + path + '/' + name[:-4]+ ' -l eng wordstrbox'
    os.system(command)

    # Shows the image in image viewer
    im.show()
    boxfilename = path + '/' + name[:-3] + 'box'
    file1 = open(boxfilename, "r")
    print('Output of Readlines after appending')
    lines = file1.readlines()
    for line in lines:
        words = line.split()
        if words[0] == 'WordStr':
            i = 1
        else:
            i = 0
        left = int(words[i])
        bottom = height - int(words[i+1])
        right = int(words[i+2])
        top = height - int(words[i+3])
        im1 = im.crop((left, top, right, bottom))
        im1.show()


    file1.close()
