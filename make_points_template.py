import cv2
import numpy as np
import sys
import math
import pickle

#crave minR = 13 maxR = 20
# pro1 minR = 15, maxR = 20

def showTilShut(img, name='test'):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def addCircle(img, i):
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        print(f"{i[0]}\t {i[1]}\t {i[2]}")
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

def make_template(arg):
    # load template image
    temp = cv2.imread(arg[1])
    ctemp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
    # find circles
    p1 = 30
    p2 = int(p1/2)
    circles = cv2.HoughCircles(ctemp,cv2.HOUGH_GRADIENT,1,20,param1=p1,param2=p2,minRadius=int(arg[3]),maxRadius=int(arg[4]))
    circles = np.uint16(np.around(circles))[0,:]
    template_points = []
    for i in circles:
        addCircle(temp, i)
        template_points.append([i[2],i[1]])
    template_points = np.asarray(template_points)
    pickle.dump(template_points, open(arg[2], "wb"))
    showTilShut(temp, name="Change the min/max radius until all knobs are circled and there are no false postitives PRESS ANY KEY TO CLOSE")

if __name__=="__main__":
    arg = sys.argv
    if '.jpg' in arg[1].lower() or '.png' in arg[1].lower() or '.jpeg' in arg[1].lower() and '.p' in arg[2] and isnumeric(arg[3]) and ismumeric(arg[4]):
        make_template(arg)
    else:
        print("Creates a template of points by searching for circles\npython make_points_template.py image_for_template template_name.p minRadius maxRadius")
