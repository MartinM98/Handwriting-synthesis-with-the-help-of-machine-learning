""" Extraction letters from images """
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    for filename in os.listdir(directory):
        ext = os.path.splitext(filename)[-1].lower()
        if ext == ".png":
            image = directory + '/' + filename
            letters = directory + '/letters'

            if not os.path.exists(letters):
                os.mkdir(letters)

            im = Image.open(image)
            width, height = im.size

            command = 'tesseract ' + image + ' ' + image[:-4] + ' -l eng makebox'
            os.system(command)

            boxfilename = image[:-3] + 'box'
            file1 = open(boxfilename, "r")
            lines = file1.readlines()
            for line in lines:
                words = line.split()
                left = int(words[1])
                bottom = height - int(words[2])
                right = int(words[3])
                top = height - int(words[4])
                im1 = im.crop((left, top, right, bottom))
                if words[0] == ':':
                    letterdir = letters + '/colon/'
                elif words[0] == '.':
                    letterdir = letters + '/dot/'
                elif words[0] == '?':
                    letterdir = letters + '/question/'
                elif words[0] == '*':
                    letterdir = letters + '/asterisk/'
                else:
                    if words[0].islower():
                        letterdir = letters + '/' + words[0] + '2/'
                    else:
                        letterdir = letters + '/' + words[0] + '/'
                if os.path.exists(letterdir):
                    count = len([sample for sample in os.listdir(letterdir)])
                else:
                    os.mkdir(letterdir)
                    count = 0
                im1.save(letterdir + str(count) + '.png')

            file1.close()
