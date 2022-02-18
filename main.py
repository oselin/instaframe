from instaframe import Instaframe


#Initialization
myphoto = Instaframe(1080,1350,100)

#Load the photos to be further manipulated
#myphoto.load_img_frompath("media/pic1.jpg")
#myphoto.load_img_frompath("media/pic2.jpg")

myphoto.load_img_frompath("media/IMG_0275.PNG")
myphoto.load_img_frompath("media/IMG_0275.PNG")

#Merge the photos
myphoto.merge("", 1, 50, 2)

#Save the result
myphoto.save('media/out.jpg')