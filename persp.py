import cv2
import numpy as np
import sys
import math

def showTilShut(img, name='test'):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def persp(arg):

    img_dst = cv2.imread(arg)
    # prepare template
    temp = cv2.imread("template4.png")
    ctemp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
    print("find circles")
    j = 0
    # while (j != 15):
    p1 = 30
    p2 = int(p1/2)
    print(p1, p2)
    circles = cv2.HoughCircles(ctemp,cv2.HOUGH_GRADIENT,1,20,param1=p1,param2=p2,minRadius=13,maxRadius=20)
    print("circles found")
    circles = np.uint16(np.around(circles))[0,:]
    template_points = []
    for i in circles:
        # draw the outer circle
        cv2.circle(temp,(i[0],i[1]),i[2],(0,255,0),2)
        # print(f"{i[0]}\t {i[1]}\t {i[2]}")
        # draw the center of the circle
        cv2.circle(temp,(i[0],i[1]),2,(0,0,255),3)
        template_points.append([i[0],i[1]])
    template_points = np.asarray(template_points)
    print(template_points)
    showTilShut(temp)

    # h, status = cv2.findHomography(pts_src, pts_dst)
    # im_dst = cv2.warpPerspective(im_src, h, size)
    # showTilShut(im_dst)




if __name__=="__main__":
    for arg in sys.argv:
        if '.jpg' in arg.lower() or '.png' in arg.lower() or '.jpeg' in arg.lower() and not "warped" in arg.lower():
            persp(arg)
