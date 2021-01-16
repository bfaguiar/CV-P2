import cv2 as cv
import numpy as np

def getPiece(x, y):
    cv.circle(image,(x,y), 35, (0,0,255), -2)
    cv.circle(image,(x,y), 25, (0,0,0), 0)
    cv.circle(image,(x,y), 20, (0,0,0), 0)

largura = 7
altura = 7
cell = 80

largura_p = (largura + 1) * cell  # + cell
altura_p = (altura + 1) * cell

image = np.zeros((altura_p, largura_p, 3), dtype=np.uint8)
image.fill(255)

titulo = "DAMAS - Computacao Visual"
cor = (255,255,255)

y0 = 0
preenchimento = 0
for j in range(0,altura + 1):
    y = j * cell
    for i in range(0,largura+1):
        x0 = i * cell
        y0 = y
        start_point = (x0,y0)

        x1 = x0 + cell
        y1 = y0 + cell
        end_point = (x1,y1)
        cv.rectangle(image, start_point, end_point, cor, 1, 0)
        image[y0:y1,x0:x1] = preenchimento
        if largura % 2: 
            if i != largura:
                preenchimento = ( 0 if ( preenchimento == 255 ) else 255 )
        else:
            if i != largura + 1:
                preenchimento = ( 0 if ( preenchimento == 255 ) else 255 )
    
    getPiece(440,120)
cv.imshow(titulo, image)
cv.waitKey()


