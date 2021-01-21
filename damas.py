import urllib.request
import cv2 as cv
import numpy as np
import time
import sys
#
#
#url='http://192.168.1.83:8080/shot.jpg' ## default IP
url='http://192.168.1.215:8080/shot.jpg' ## default IP
if len(sys.argv) == 2:
    url = "http://192.168.1."+ sys.argv[1] + ":8080/shot.jpg" ## pass IP from the command line

while True:

    imgResp = urllib.request.urlopen(url) ## getting the image from the IP Camera
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8) #convert into array
    img = cv.imdecode(imgNp,-1) # decoding array to be usable for OpenCV
    
    height, width, nchannels = img.shape
    rendering2D = np.zeros((height, width), dtype=np.uint8)
    rendering2D.fill(255)

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (7, 7), 0)
    edged = cv.Canny(blur, 75, 200)
    cv.imshow("ola", edged)
    contours, hierarchy = cv.findContours(edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    array = []

    for cnt in contours:
        approx = cv.approxPolyDP(cnt, 0.009*cv.arcLength(cnt,True), True)
        if len(approx)==4: 
            cv.drawContours(img,[cnt],0,(0,0,255),5) #Azul
            # GET COORDINATES
            n = approx.ravel()
            i = 0
            c = []
            for j in n:
                if(i % 2 == 0): 
                    x = n[i] 
                    y = n[i + 1] 
                    
                    # String containing the co-ordinates. 
                    string = str(x) + " " + str(y)  
                    c.append(string)
                    if(i == 0): 
                        # text on topmost co-ordinate. 
                        cv.putText(img, "Arrow tip", (x, y), 
                                        cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))  
                    else: 
                        # text on remaining co-ordinates. 
                        cv.putText(img, string, (x, y),  
                                cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))  
                i = i + 1
            if (cv.contourArea(cnt) < 15000):
                array.append(c)
    for a in array:
        p1 = a[0 ].split(" ")
        coor1 = (int(p1[0]), int(p1[1]))
        p2 = a[2 ].split(" ")
        coor2 = (int(p2[0]), int(p2[1]))
        cv.rectangle(rendering2D, coor1, coor2, (0, 0, 255), -1)
    cv.imshow("Final Image", img)  
    cv.imshow("LOLZ", rendering2D)
    #cv.drawContours(img, contours, -1, (0,255,0), 3)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
