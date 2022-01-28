import cv2
import numpy as np

class Instaframe:
    def __init__(self, width = 0, height = 0, border = 0):
        self.width  = width
        self.height = height
        self.border = border
        self.frame  = np.zeros([self.height, self.width, 3], dtype=np.uint8)
        self.frame.fill(255)
        self.img    = []

    #Private methods
    def __update_frame(self):
        self.frame = np.zeros([self.height, self.width, 3], dtype=np.uint8)
        self.frame.fill(255)

    def __resize(self, index):
        scale_percent = (self.width-2*self.border)/self.img[index].shape[1]
        new_width  = int(self.img[index].shape[1] * scale_percent)
        new_height = int(self.img[index].shape[0] * scale_percent)

        self.img[index] =  cv2.resize(self.img[index], [new_width, new_height], interpolation = cv2.INTER_AREA)

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
        self.img.append(img)
    
    def set_image_frompath(self, path):
        #check if the image actually exists
        self.img.append(cv2.imread(path, cv2.IMREAD_UNCHANGED))
    
    def show(self, index = 0):
        if len(self.img) > 0:
            cv2.imshow("Photo", self.img[index])
    def show_frame(self):
        cv2.imshow("Photo",self.frame)

    def get_dim(self):
        print(self.height,self.width)

    def save(self, mode):
        self.__resize(0)
        self.__resize(1)
        img = self.compose(mode)
        return img

    def draw_border(color):
        return

    def compose(self,mode = ""):
        img = np.zeros([self.frame.shape[0], self.frame.shape[1],3], dtype=np.uint8)
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
                    
        return img
    