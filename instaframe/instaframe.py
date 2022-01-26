import cv2
import numpy as np

class Instaframe:
    def __init__(self):
        self.width  = 0
        self.height = 0
        self.border = 0
        self.frame  = np.zeros([self.width, self.height, 3], dtype=np.uint8)
        self.img    = np.zeros([self.width, self.height, 3], dtype=np.uint8)
    
    def update_frame(self):
        self.frame = np.zeros([self.width, self.height, 3], dtype=np.uint8)
        self.frame.fill(255)

    def set_frame(self,width, height):
        self.width  = width
        self.height = height
        self.update_frame()
    
    def set_img(self, img):
        self.img = img
    
    def resize(self, img):
        scale_percent = (self.width-2*self.border)/self.width
        new_width  = int(img.shape[1] * scale_percent / 100)
        new_height = int(img.shape[0] * scale_percent / 100)
        self.img =  cv2.resize(img, (new_width, new_height), interpolation = cv2.INTER_AREA)


