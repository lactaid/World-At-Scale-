import cv2
from object_detector import *
import numpy as np
from tkinter import *

def medir(path):

    a = path
    b = '"'
    a = b+a+b
    img = cv2.imread(a)

    # Load Object Detector
    detector = HomogeneousBgDetector()
    ...
    contours = detector.detect_objects(img)
    ...

    # Draw objects boundaries
    for cnt in contours:
        # Get rect
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect
        # Display rectangle
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
        cv2.polylines(img, [cnt], True, (255, 0, 0), 2)
        print("box: ", box)
    print("x: ", x)
    print("y: ", y)
    print("w: ", w)
    print("h: ", h)
    cv2.imshow("Image", img)
    cv2.waitKey(0)


# d = "C:/Users/gandr/Documents/vsproj/GitHub/World-At-Scale-/medidor objetos/images/test4.jpg"
#
# medir(d)

