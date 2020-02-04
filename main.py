import cv2
import numpy as np
import sys
import math
import pickle

def showTilShut(img, name='test'):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def addCircle(img, i):
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        print(f"{i[0]}\t {i[1]}\t {i[2]}")
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

def getPatch(arg):
    # load template
    template_points = pickle.load(open("pro1.p", "rb"))
    # load image & preprocess
    img = cv2.imread(arg)
    cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # find circles, pots
    circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,1,20,param1=80,param2=18,minRadius=0,maxRadius=30)
    circles = np.uint16(np.around(circles))[0,:]
    circle_points = []
    for i in circles:
        circle_points.append([i[0], i[1]])
        addCircle(img, i)
    showTilShut(img)
    circle_points = np.asarray(circle_points)
    print(circle_points, type(circle_points), circle_points.shape)
    print(template_points, type(template_points), template_points.shape)

    # h, status = cv2.findHomography(template_points, circle_points)
    # size = (int(img.shape[1]/2), int(img.shape[0]/2))
    # im_dst = cv2.warpPerspective(img, h, size)
    # showTilShut(im_dst)
    # showTilShut(img)


if __name__=="__main__":
    for arg in sys.argv:
        if '.jpg' in arg.lower() or '.png' in arg.lower() or '.jpeg' in arg.lower() and not "warped" in arg.lower():
            getPatch(arg)
