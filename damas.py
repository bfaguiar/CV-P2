# Paulo Sousa, 80000
# Bruno Aguiar, 80177
import urllib.request
import cv2 as cv
import numpy as np
import time
import sys 

url='http://192.168.1.215:8080/shot.jpg' ## default IP
if len(sys.argv) == 2:
    url = "http://192.168.1."+ sys.argv[1] + ":8080/shot.jpg" ## pass IP from the command line

x_verde, y_verde, raio_verde = 0, 0, 0 
x_azul, y_azul, r_azul = 0, 0, 0
while True:

    imgResp = urllib.request.urlopen(url) ## getting the image from the IP Camera
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8) #convert into array
    img = cv.imdecode(imgNp,-1) # decoding array to be usable for OpenCV
    img = img[0:3000, 300:1550]
    height, width, nchannels = img.shape
    rendering2D = np.zeros((height, width, 3), dtype=np.uint8)
    rendering2D[:] = (255, 255, 255)

    colored = cv.cvtColor(img, cv.COLOR_BGR2HSV) ## color for detect circles 
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (7, 7), 0)
    edged = cv.Canny(blur, 100, 200)
    cv.imshow("Edge Canny", edged) 
    contours, hierarchy = cv.findContours(edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    array = []

    for cnt in contours:
        approx = cv.approxPolyDP(cnt, 0.009*cv.arcLength(cnt,True), True)
        if len(approx)>3 and len(approx) < 10: 
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
            array.append(c)

    for a in array:
        p1 = a[0 ].split(" ")
        coor1 = (int(p1[0]), int(p1[1]))
        p2 = a[2 ].split(" ")
        coor2 = (int(p2[0]), int(p2[1]))
        cv.rectangle(rendering2D, coor1, coor2, (0, 0, 0), -1)
    
    # Set range for green color and  
    # define mask 
    green_lower = np.array([25, 52, 72], np.uint8) 
    green_upper = np.array([85, 255, 255], np.uint8) 
    green_mask = cv.inRange(colored, green_lower, green_upper) 
    res2 = cv.bitwise_and(colored, colored, mask=green_mask)
    res2 = cv.GaussianBlur(res2, (7, 7), 0)
    res2 = cv.Canny(res2, 100, 200)
    kernel = np.ones((5,5),np.uint8)
    res2 = cv.dilate(res2, kernel, iterations=2)
    circles = cv.HoughCircles(res2, cv.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            x_verde, y_verde, raio_verde = i  
            cv.circle(rendering2D, (x_verde, y_verde), 50, (0, 255, 0), -1)  

    # Set range for blue color and  
    # define mask 
    blue_lower = np.array([94, 70, 2], np.uint8) 
    blue_upper = np.array([120, 200, 200], np.uint8) 
    blue_mask = cv.inRange(colored, blue_lower, blue_upper) 
    res3 = cv.bitwise_and(colored, colored, mask=blue_mask)
    res3 = cv.GaussianBlur(res3, (7, 7), 0)
    res3 = cv.Canny(res3, 100, 200)
    kernel = np.ones((5,5),np.uint8)
    res3 = cv.dilate(res3, kernel, iterations=2)
    circles = cv.HoughCircles(res3, cv.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            x_azul, y_azul, r_azul = i
            cv.circle(rendering2D, (x_azul, y_azul), 50, (255, 0, 0), -1) 
    print (circles)
    cv.imshow("green Mask", res2)
    cv.imshow("Azul Mask", res3)
    cv.imshow("Edge Detection Image", img)  
    cv.imshow("Checkers Game", rendering2D)


    if cv.waitKey(1) & 0xFF == ord('q'):
        break
