import cv2
import numpy as np
import sys
import math
from sklearn.cluster import KMeans

def showTilShut(name, img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def hough(arg):
    # load image
    img = cv2.imread(arg)
    scale_percent = 30 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    # get region of synth
    light_orange = (0, 100, 200)
    dark_orange = (50, 150, 255)
    white1 = (125, 125, 255)
    white2 = (0, 0, 0)
    import matplotlib.pyplot as plt
    from matplotlib.colors import hsv_to_rgb
    # lo_square = np.full((10, 10, 3), light_orange, dtype=np.uint8) / 255.0
    # do_square = np.full((10, 10, 3), dark_orange, dtype=np.uint8) / 255.0
    # lo_square = np.full((10, 10, 3), white1, dtype=np.uint8) / 255.0
    # do_square = np.full((10, 10, 3), white2, dtype=np.uint8) / 255.0
    # plt.subplot(1, 2, 1)
    # plt.imshow(hsv_to_rgb(do_square))
    # plt.subplot(1, 2, 2)
    # plt.imshow(hsv_to_rgb(lo_square))
    # plt.show()
    # exit()
    mask = cv2.inRange(img, light_orange, dark_orange)
    mask2 = cv2.inRange(img, white2, white1)

    print (mask.shape)
    xMin = mask.shape[0]
    xMax = 0
    yMin = mask.shape[1]
    yMax = 0
    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            if(mask[y][x] == 255):
                if y < yMin: yMin = y
                if y > yMax: yMax = y
                if x < xMin: xMin = x
                if x > xMax: xMax = x
    print(f"{xMin}\t{xMax}\t{yMin}\t{yMax}")
    height = -1*(yMin - yMax)
    width = (xMin - xMax)*-1
    print(f"H: {height}\tW: {width}")
    # minRadius=20,maxRadius=27
    # H: 557	W: 1111
    minR = int(((20/557)*height + (20/1111)*width)/2)
    maxR = int(((27/557)*height + (27/1111)*width)/2)
    # remove the top area
    yMin = int(yMin + height * 0.2)

    # result = cv2.bitwise_and(img, img, mask=mask)
    # showTilShut('test',mask2)
    cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    # find circles
    print("find circles")
    circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,1,20,param1=80,param2=18,minRadius=minR,maxRadius=maxR)
    print("circles found")
    circles = np.uint16(np.around(circles))[0,:]
    for i in circles:
        #filter
        if (i[0] > xMin and i[0] < xMax) and (i[1] > yMin and i[1] < yMax):
            #search for the black dot
            xdot = 0
            ydot = 0

            # draw the outer circle
            cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
            print(f"{i[0]}\t {i[1]}\t {i[2]}")
            # draw the center of the circle
            cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

            # draw the outer circle
            cv2.circle(mask2,(i[0],i[1]),i[2],(0,255,0),2)
            print(f"{i[0]}\t {i[1]}\t {i[2]}")
            # draw the center of the circle
            cv2.circle(mask2,(i[0],i[1]),2,(0,0,255),3)

    showTilShut('test',img)


if __name__=="__main__":
    for arg in sys.argv:
        if '.jpg' in arg.lower() or '.png' in arg.lower() or '.jpeg' in arg.lower() and not "warped" in arg.lower():
            hough(arg)
