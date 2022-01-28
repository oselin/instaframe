import cv2
import numpy as np
import math


class Instaframe:
    def __init__(self, width = 0, height = 0, border = 0, color = [255,255,255]):
        self.width  = None
        self.height = None
        self.border = None
        self.color  = []
        self.img    = []
        self.frame  = np.zeros([0,0,0])

        self.set_frame(width, height)
        self.set_border(border)
        self.set_color(color)
        self.merge()

    #Private methods-----------------------------
    def __update_frame(self):
        self.frame = np.zeros([self.height, self.width, 3], dtype=np.uint8)

        for i in range(len(self.color)):
            self.frame[:,:,i] = self.color[i]

    def __resize(self, index):
        scale_percent = (max(self.width,self.height)-2*self.border)/max(self.img[index].shape)
        new_width  = int(self.img[index].shape[1] * scale_percent)
        new_height = int(self.img[index].shape[0] * scale_percent)

        self.img[index] =  cv2.resize(self.img[index], [new_width, new_height], interpolation = cv2.INTER_AREA)

    def __set_rounded_corners(self, img, lim, radius):
        for x in np.arange(0,radius+0.01,0.01):
            y_corner = math.ceil(math.sqrt(radius**2-x**2))
            
            x = math.ceil(x)
            for y in range(radius-y_corner):
                #Top-left corner
                img[lim[0]+y, lim[1]+radius-x, :] = self.frame[0,0,:]

                #Top-right corner
                img[lim[0]+y, self.frame.shape[1]-lim[1]-radius+x, :] = self.frame[0,0,:]

                #Bottom-left
                img[self.frame.shape[0]-lim[0]-y, lim[1]+radius-x, :] = self.frame[0,0,:]
            
                #Bottom-right
                img[self.frame.shape[0]-lim[0]-y, self.frame.shape[1]-lim[1]-radius+x, :] = self.frame[0,0,:]


        return img

    def __is_img_valid(self, img):
        if len(self.img) > 0:
            if (self.img[-1].shape != img.shape or img.size < 0):
                return 0
        return 1
    
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
             
    def show(self, index = 0):
        if (index >= 0 and len(self.img) < index):
            cv2.imshow(str(index) + "-loaded photo", self.img[index])
        elif (index == -1):
            cv2.imshow("Output photo", self.output)
        else:
            raise Exception("Image index wrong or photo not loaded.")
    
    def show_frame(self):
        cv2.imshow("Image frame",self.frame)

    def see(self):
        return self.output

    def get_dim(self):
        return [self.height,self.width]

    def merge(self, mode="", roundedCorners = 0, radius = 20, border = 0):
        if (len(self.img) == 0):
            #Create an empty image
            img = np.zeros([self.frame.shape[0], self.frame.shape[1],3], dtype=np.uint8)
            self.output = img
            return

        if (len(self.img) < 2 and mode != "" ):
            raise Exception("Not enough images have been loaded.")
        
        for i in range(len(self.img)):
            self.__resize(i)

        #Create an empty image
        img = np.zeros([self.frame.shape[0], self.frame.shape[1],3], dtype=np.uint8)

        #Find the frame dimensions
        lim = [int((self.frame.shape[0]-self.img[0].shape[0])/2), int((self.frame.shape[1]-self.img[0].shape[1])/2)]
   
        #Image composition
        threshold = 0
        for row in range(self.frame.shape[0]):
            for column in range(self.frame.shape[1]):
                if row < lim[0] or row >= (self.frame.shape[0]-lim[0]) or column < lim[1] or column >= (self.frame.shape[1]-lim[1]):
                    img[row,column,:] = self.frame[row,column,:]
                
                else:
                    irow    = row   -lim[0]
                    icolumn = column-lim[1]

                    if mode == "":
                        img[row, column, :] = self.frame[row, column, :]

                    elif mode == '|':
                        if (column < self.frame.shape[1]/2):
                            img[row, column, :] = self.img[0][irow, icolumn, :]
                        else:
                            img[row, column, :] = self.img[1][irow, icolumn, :]

                    elif mode == '/':       
                        if (icolumn == 0):
                            threshold -= 1
                        if (irow == 0 and icolumn == 0):
                            threshold = (min(self.img[0].shape[0],self.img[0].shape[1])+self.frame.shape[1]-2*lim[1])/2   

                        if (icolumn < threshold):
                            img[row, column, :] = self.img[0][irow, icolumn, :]
                        else:
                            img[row, column, :] = self.img[1][irow, icolumn, :]
                        
                    elif mode == '-':
                        if (row < self.frame.shape[0]/2):
                            img[row, column, :] = self.img[0][irow, icolumn, :]
                        else:
                            img[row, column, :] = self.img[1][irow, icolumn, :]

                    elif mode == '\\':
                        if (icolumn == 0):
                            threshold += 1
                        if (irow == 0 and icolumn == 0):
                            threshold = (-min(self.img[0].shape[0],self.img[0].shape[1])+self.frame.shape[1])/2

                        if (column < threshold):
                            img[row, column, :] = self.img[0][irow, icolumn, :]
                        else:
                            img[row, column, :] = self.img[1][irow, icolumn, :]

                    else:
                        raise ""
        
        if roundedCorners:
            img = self.__set_rounded_corners(img, lim, radius)
        self.output = img

    def save(self, path = 'output.jpg'):
        try:
            cv2.imwrite(path, self.output)
        except:
            raise Exception("Error, image can't be saved.")