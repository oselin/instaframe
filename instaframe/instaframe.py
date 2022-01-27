import cv2
import numpy as np

class Instaframe:
    def __init__(self, width = 0, height = 0, border = 0):
        self.width  = width
        self.height = height
        self.border = border
        self.frame  = np.zeros([self.width, self.height, 3], dtype=np.uint8)
        self.frame.fill(255)
        self.img    = []

    #Private methods
    def __update_frame(self):
        self.frame = np.zeros([self.width, self.height, 3], dtype=np.uint8)
        self.frame.fill(255)

    def __resize(self, index):
        scale_percent = (self.width-2*self.border)/self.img[index].shape[1]
        new_width  = int(self.img[index].shape[1] * scale_percent)
        new_height = int(self.img[index].shape[0] * scale_percent)

        self.img[index] =  cv2.resize(self.img[index], [new_width, new_height], interpolation = cv2.INTER_AREA)
        print(self.img[index].shape)

    #Public methods
    def set_frame(self,width, height):
        try:
            if (width > 0 and height > 0):
                self.width  = width
                self.height = height
                self.__update_frame()
        except err:
            raise ""
    
    def set_border(self, border):
        try:
            if (border > 0):
                self.border = border
        except err:
            raise ""
    
    def set_img(self, img):
        #check if img is an image
        print(img.shape)
        self.img.append(img)
    
    def set_image_frompath(self, path):
        #check if the image actually exists
        self.img.append(cv2.imread(path, cv2.IMREAD_UNCHANGED))
        print(self.img[-1].shape)
    
    def show(self, index = 0):
        if len(self.img) > 0:
            cv2.imshow("Photo", self.img[index])
    def show_frame(self):
        cv2.imshow("Photo",self.frame)

    def get_dim(self):
        print(self.width,self.height)

    def save(self, mode):
        self.__resize(0)
        self.__resize(1)
        img = self.compose(mode)
        return img

    def draw_border(color):
        return

    def compose(self,mode = ""):
        img = np.zeros([self.frame.shape[0], self.frame.shape[1],3], dtype=np.uint8)
        lim = [int((self.frame.shape[0]-self.img[0].shape[0])/2), int((self.frame.shape[1]-self.img[1].shape[0])/2)]
        #Image composition
        for layer in range(3):
            for row in range(self.frame.shape[1]):
                for column in range(self.frame.shape[0]):
                    #print (row,column)
                    #print("CHECK:",self.frame.shape[0]-2*self.border)
                    if (row < lim[1] or row > (self.frame.shape[1]-lim[1])) or (column < lim[0] or column > (self.frame.shape[0]-lim[0])):
                        img[column,row,layer] = self.frame[column,row,layer]
                    else:
                        if mode == "":
                            img[column, row, layer] = self.frame[column, row, layer]

                        elif mode == '|':
                            #print(row,column)
                            if (column < self.frame.shape[0]/2):
                                img[column, row, layer] = self.img[0][column-lim[0], row-lim[1], layer]
                            else:
                                img[column, row, layer] = self.img[1][column-lim[0], row-lim[1], layer]

                        elif mode == '/':
                            if (row >= column):
                                img[row,column,layer] = self.img[0][row-self.border,column-self.border,layer]
                            else:
                                img[row,column,layer] = self.img[1][row-self.border,column-self.border,layer]

                        elif mode == '-':
                            if (row < self.frame.shape[1]/2):
                                img[row,column,layer] = self.img[0][row-self.border,column-self.border,layer]
                            else:
                                img[row,column,layer] = self.img[1][row-self.border,column-self.border,layer]

                        elif mode == '\\':
                            if (row <= column ):
                                img[row,column,layer] = self.img[0][row-self.border,column-self.border,layer]
                            else:
                                img[row,column,layer] = self.img[1][row-self.border,column-self.border,layer]

                        else:
                            raise ""


        return img
    

