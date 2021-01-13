#
#
import urllib.request
import cv2 as cv
import numpy as np
import time
import sys

url='http://192.168.1.83:8080/shot.jpg' ## default IP

if len(sys.argv) == 2:
    url = sys.argv[1] + "/shot.jpg" ## pass IP from the command line

while True:

    imgResp = urllib.request.urlopen(url) ## getting the image from the IP Camera
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8) #convert into array
    img = cv.imdecode(imgNp,-1) # decoding array to be usable for OpenCV
    
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (7, 7), 0)
    edged = cv.Canny(blur, 75, 200)
    cv.imshow("ola", edged)
    
    contours, hierarchy = cv.findContours(edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img, contours, -1, (0,255,0), 3)
    cv.imshow("Normal", img) # show the normal image

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
