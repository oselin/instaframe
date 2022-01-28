from instaframe import Instaframe
import time as t
import numpy as np
import cv2
import sys

#Initialization
myphoto = Instaframe(1080,1350,100)

#Load the photos to be further manipulated
myphoto.load_img_frompath("media/pic.jpg")
myphoto.load_img_frompath("media/pic2.jpg")

#Merge the photos
myphoto.merge("/", 1, 50, 2)

#Save the result
myphoto.save('media/out.jpg')