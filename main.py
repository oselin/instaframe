from instaframe import Instaframe
import time as t
import numpy as np
import cv2
import sys
myphoto = Instaframe(1080,1350)

myphoto.set_border(100)

#myphoto.set_image_frompath('pic.jpg')

#myphoto.resize()

#myphoto.show_frame()
myphoto.set_image_frompath("media/pic.jpg")
myphoto.set_image_frompath("media/pic2.jpg")

myphoto.get_dim()
cv2.imwrite('media/out.jpg', myphoto.save("/"))

