import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.filters import gabor
from skimage import io,filters
import matplotlib.pyplot as plt
from skimage import img_as_ubyte
from skimage.util import invert
from PIL import Image
from skimage.morphology import skeletonize
import scipy.misc
from tkinter import filedialog
from tkinter import *
import os

def nothing(x):
    pass

def nothing2(one,two):
    global result
    global cv_image
    result=np.bitwise_and(result,cv_image)
    
root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
path = root.filename
path2 = os.path.splitext(os.path.split(root.filename)[1])[0]
root.destroy()
img2 = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('trackbar')

cv2.createTrackbar('theta','trackbar',25,300,nothing)
cv2.createTrackbar('lamda','trackbar',16,300,nothing)
cv2.createTrackbar('gamma','trackbar',9,300,nothing)
cv2.createTrackbar('phi','trackbar',8,300,nothing)
cv2.createButton('save control points',nothing2,['test','test2'],cv2.QT_PUSH_BUTTON)


img = cv2.imread(root.filename)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
result=np.zeros(shape=img.shape)
result = img_as_ubyte(result)
result=invert(result)
while(1):
    cv2.imshow('trackbar',img2)
    k = cv2.waitKey(1) & 0xFF
    if k == 97:
        break

    theta=cv2.getTrackbarPos('theta','trackbar')*0.01*np.pi
    lamda=cv2.getTrackbarPos('lamda','trackbar')*0.01*np.pi
    gamma=cv2.getTrackbarPos('gamma','trackbar')*0.1
    phi=cv2.getTrackbarPos('phi','trackbar')*0.1



    img = cv2.imread(path)

    
    plt.imshow(img, cmap='gray')
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    filt_real,filt_imag=gabor(img,frequency=1/lamda,theta=theta )

    cv2.imshow('Original Img.', img)
    
    cv_image = img_as_ubyte(filt_imag)
    cv_image=invert(cv_image)

    cv_image2=cv2.resize(cv_image,(500,500))
    cv2.imshow('Filtered 2', cv_image2)
    
cv2.destroyAllWindows()

cv2.imshow('END',result)
result2=cv2.resize(result,(500,500))
cv2.imshow('END2',result2)
cv2.waitKey()
cv2.imwrite(path2+'_control_points.png',result)

