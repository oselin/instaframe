import cv2
import numpy as np
import math


class Instaframe:
    def __init__(self, width = 0, height = 0, border = 0, color = [255,255,255]):
        self.width  = None
        self.height = None
        self.border = None
        self.isvertical = 0
        self.ratio = 1
        self.color  = []
        self.img    = []
        self.frame  = np.zeros([0,0,0])
        self.mode = ""
        
        self.set_border(border)
        self.set_frame(width, height)
        self.set_color(color)
        self.merge()
        
    def __update_frame(self):
        self.frame = np.zeros([self.height, self.width, 3], dtype=np.uint8)

        for i in range(len(self.color)):
            self.frame[:,:,i] = self.color[i]

    def __get_ratio(self, img):
        try:
            return img.shape[0]/img.shape[1]
        except:
            raise Exception("Image seems empty.")

    def __is_vertical(self, img):
        if (img.shape[0] >= img.shape[1]):
            return 1
        return 0

    def __is_img_valid(self, img):
        if (len(self.img) < 1):
            self.isvertical = self.__is_vertical(img)
            self.ratio = self.__get_ratio(img)
        
        if (img.size < 0 or self.__is_vertical(img) != self.isvertical or self.__get_ratio(img) != self.ratio):
            return 0

        return 1
    
    def __resize(self, index):
        if (self.img[index].shape[0] > self.img[index].shape[1]):
            scale_percent = (self.height-2*self.border)/max(self.img[index].shape)
        else:
            scale_percent = (self.width-2*self.border)/max(self.img[index].shape)

        new_width  = int(self.img[index].shape[1] * scale_percent)
        new_height = int(self.img[index].shape[0] * scale_percent)

        self.img[index] =  cv2.resize(self.img[index], [new_width, new_height], interpolation = cv2.INTER_AREA)
    
    def __set_threshold(self):
        threshold = [0,0]

        if   (self.mode == "|"):
            threshold = [0, self.img[0].shape[1]/2]

        elif (self.mode == "/"):
            p = abs(self.img[0].shape[0] - self.img[0].shape[1])/2
            if self.isvertical:
                threshold = [p, self.img[0].shape[1]]
            else:
                threshold = [0, self.img[0].shape[1] - p]

        elif (self.mode == "-"):
            threshold = [self.img[0].shape[0]/2, 0]
        
        return threshold

    def __update_threshold(self, threshold):
        if   (self.mode == "/"):
            threshold[0] += 1
            threshold[1] -= 1
        elif (self.mode == "\\"):
            threshold[0] += 1
            threshold[1] += 1

        return threshold

    def __set_rounded_corners(self, lim, radius):
        for x in np.arange(0, radius+0.01, 0.01):
            y_corner = math.ceil(math.sqrt(radius**2-x**2))
            
            x = math.ceil(x)
            for y in range(radius-y_corner):
                #Top-left corner
                self.output[lim[0]+y, lim[1]+radius-x, :] = self.frame[0,0,:]

                #Top-right corner
                self.output[lim[0]+y, self.frame.shape[1]-lim[1]-radius+x, :] = self.frame[0,0,:]

                #Bottom-left
                self.output[self.frame.shape[0]-lim[0]-y, lim[1]+radius-x, :] = self.frame[0,0,:]
            
                #Bottom-right
                self.output[self.frame.shape[0]-lim[0]-y, self.frame.shape[1]-lim[1]-radius+x, :] = self.frame[0,0,:]
    
    def __draw_border(self, border):
        if (self.mode == ""):
            return

        threshold = self.__set_threshold()
        
        #Convert the border in an odd number
        if (border%2 == 0): border += 1
        
        for i in range(border-1, border+1,1):
            print(i)

    
    #Public methods------------------------------
    def set_frame(self, width, height):
        if (width >= 0 and height >= 0):
            self.width  = int(width)
            self.height = int(height)
            self.__update_frame()
        else:
            raise Exception("Values must be greater or equal than 0.")
    
    def set_color(self, color):
        try:
            if (len(color) == 3):
                self.color = color
                self.__update_frame()
        except:
            raise Exception("Color must be an array in RBG color code.")
    
    def set_border(self,border):
        try:
            border = int(border)
            if (border >= 0):
                self.border = border
        except:
            raise Exception("Border must be a number.")

    def load_img(self, img):
        if self.__is_img_valid(img):
            self.img.append(img)            
        else:
            raise Exception("Image is empty, missing or has wrong dimensions.")
    
    def load_img_frompath(self, path):
        try:
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if self.__is_img_valid(img):
                self.img.append(img)
            else:
                raise Exception("Image is empty or has wrong dimensions")
        except:
                raise Exception("Photo missing.")
             
    def merge(self, mode="", roundedCorners = 0, border = 0):

        #Create an empty image
        self.output = self.frame

        #Update the merge mode
        if (mode in ["|","/","-","\\"]): self.mode = mode

        if (len(self.img) == 0):
            return

        if (len(self.img) < 2 and self.mode != "" ):
            raise Exception("Not enough images have been loaded.")
        
        #Resize all images
        for i in range(len(self.img)):
            self.__resize(i)

        #Find the frame dimensions
        lim = [int((self.frame.shape[0]-self.img[0].shape[0])/2), int((self.frame.shape[1]-self.img[0].shape[1])/2)]
   
        #Image composition
        threshold = self.__set_threshold()

        for row in range(self.img[0].shape[0]):
            a_row = row + lim[0]
            for column in range(self.img[0].shape[1]):
                a_column = column + lim[1]
                if (self.mode == '|'):
                    w = self.img[0].shape[1]
                    self.output[lim[0]:-lim[0], lim[1]:lim[1]+int(w/2), :]   = self.img[0][:, 0:int(w/2), :]
                    self.output[lim[0]:-lim[0], lim[1]+int(w/2):lim[1]+w, :] = self.img[1][:, int(w/2):w, :]
                    break

                elif (self.mode == '-'):
                    h = self.img[0].shape[0]
                    self.output[lim[0]:lim[0]+int(h/2), lim[1]:-lim[1], :]   = self.img[0][0:int(h/2), :, :]
                    self.output[lim[0]+int(h/2):lim[0]+h, lim[1]:-lim[1], :] = self.img[1][int(h/2):h, :, :]
                    break

                elif (self.mode == '/' or self.mode == "\\"):    
                    if (column < threshold[1] or row < threshold[0]):
                        self.output[a_row, a_column, :] = self.img[0][row, column, :]
                    else:
                        self.output[a_row, a_column, :] = self.img[1][row, column, :]
                        threshold = [threshold[0], threshold[1]]

                else:
                    self.output[:, :, :] = self.img[0][:, :, :]
                    break

            if (self.mode == "|" or self.mode == "-" or self.mode == ""): break
            if (row > threshold[0]): threshold = self.__update_threshold(threshold)

        if (roundedCorners): self.__set_rounded_corners(lim, roundedCorners)
        self.__draw_border(border)
            
    def save(self, path = 'output.jpg'):
        try:
            cv2.imwrite(path, self.output)
        except:
            raise Exception("Error, image can't be saved.")