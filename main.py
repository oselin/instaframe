from instaframe import Instaframe


#Initialization
myphoto = Instaframe(1080,1350,100)

#Load the photos to be further manipulated
myphoto.load_img_frompath("media/pic5.PNG")
myphoto.load_img_frompath("media/pic6.PNG")

#Merge the photos
myphoto.merge("\\", 1, 50, 2)

#Save the result
myphoto.save('media/out.jpg')