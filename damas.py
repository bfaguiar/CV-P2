#
import urllib.request
import cv2 as cv
import numpy as np
import time
import sys
#
#
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

    for cnt in contours:
        approx = cv.approxPolyDP(cnt, 0.009*cv.arcLength(cnt,True), True)
        if len(approx)==5: 
            print("pentagon") 
            cv.drawContours(img,[cnt],0,255,5) 
        elif len(approx)==3: 
            print("triangle") 
            cv.drawContours(img,[cnt],0,(0,255,0),5) 
        elif len(approx)==4: 
            print("square") 
            cv.drawContours(img,[cnt],0,(0,0,255),5) 
        elif len(approx) == 9: 
            print("half-circle") 
            cv.drawContours(img,[cnt],0,(255,255,0),5) 
        elif len(approx) > 15: 
            print("circle") 
            cv.drawContours(img,[cnt],0,(0,255,255), 5)  
        
        # GET COORDINATES
        n = approx.ravel()
        i = 0
        for j in n:
            if(i % 2 == 0): 
                x = n[i] 
                y = n[i + 1] 
    
                # String containing the co-ordinates. 
                string = str(x) + " " + str(y)  
    
                if(i == 0): 
                    # text on topmost co-ordinate. 
                    cv.putText(img, "Arrow tip", (x, y), 
                                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))  
                else: 
                    # text on remaining co-ordinates. 
                    cv.putText(img, string, (x, y),  
                            cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))  
            i = i + 1
    
    cv.imshow("Final Image", img)  

    #cv.drawContours(img, contours, -1, (0,255,0), 3)
    #cv.imshow("Normal", img) # show the normal image

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
