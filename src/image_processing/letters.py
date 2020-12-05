""" Extraction letters from images """
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image


def check_char(path, char: str):
    """
    Function for replacing problematic characters with their string description for folder creation
    Args:
        path (str): Parent directory of the new folder.
        char (str): Character to check and replace.
    Returns:
        (str): Complete path for the new folder.
    """
    if char == ':':
        return path + '/colon/'
    elif char == '.':
        return path + '/dot/'
    elif char == '?':
        return path + '/question/'
    elif char == '*':
        return path + '/asterisk/'
    else:
        if char.islower():
            return path + '/' + char + '2/'
        else:
            return path + '/' + char + '/'


def extract(path=None):
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    if path is None:
        path = directory
    letters = path + '/letters_dataset'
    if not os.path.exists(letters):
        os.mkdir(letters)
    for filename in os.listdir(directory):
        ext = os.path.splitext(filename)[-1].lower()
        if ext == ".png":
            image = directory + '/' + filename

            im = Image.open(image)
            width, height = im.size

            command = 'tesseract ' + image + ' ' + image[:-4] + ' -l engnew makebox'
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
                letterdir = check_char(letters, words[0])
                if os.path.exists(letterdir):
                    count = len([sample for sample in os.listdir(letterdir)])
                else:
                    os.mkdir(letterdir)
                    count = 0
                im1.save(letterdir + str(count) + '.png')

            file1.close()
            return letters


def correct(path=None):
    for r, d, f in os.walk(path):
        for folder in d:
            root = tk.Tk()
            root.withdraw()
            directory = os.path.join(r, folder)
            filestring = filedialog.askopenfilenames(initialdir=directory, title='Select incorrectly recognized letters')
            files = root.tk.splitlist(filestring)
            for file in files:
                os.remove(file)
            if not os.listdir(directory):
                os.rmdir(directory)
            else:
                i = 0
                for filename in sorted(os.listdir(directory), key=lambda x: int(x[:-4])):
                    os.rename(directory + '/' + filename, directory + '/' + str(i) + '.png')
                    i += 1


if __name__ == '__main__':
    letters = extract()
    correct(letters)
