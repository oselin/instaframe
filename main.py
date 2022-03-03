from instaframe import Instaframe


#Initialization
#Parameters: width, height, min_border, color(RGB array: e.g. [255,255,255])
myphoto = Instaframe(1080,1350,100)

#Load the photos to be further manipulated
myphoto.load_img_frompath("media/pic1.jpg")
myphoto.load_img_frompath("media/pic2.jpg")

#myphoto.load_img_frompath("media/pic5.PNG")
#myphoto.load_img_frompath("media/pic6.PNG")

#Merge the photos
myphoto.merge("-", 50, 6)

#Save the result
myphoto.save('media/out.jpg')