import cv2
import numpy as np
import math


# import matplotlib.pyplot as plt

def rectify(h):
    h = h.reshape((4,2))
    hnew = np.zeros((4,2),dtype = np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h,axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew
# add image here.
# We can also use laptop's webcam if the resolution is good enough to capture
# readable document content
# resize image so it can be processed
# choose optimal dimensions such that important content is not lost


def canny_img(image,ite,t_lower,t_upper):
    # creating copy of original image
    image = cv2.resize(image, (1500, 880))
    orig = image.copy()
    
    # convert to grayscale and blur to smooth
    blurred = cv2.GaussianBlur(image, (5, 5), 0)

    kernel = np.ones((10,10),np.uint8)
    blurred = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel, iterations= ite)
    morphing = blurred

    # apply Canny Edge Detection
    edged = cv2.Canny(blurred, t_lower, t_upper, apertureSize=7)
    orig_edged = edged.copy()

    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    (contours, _) = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # get approximate contour
    for c in contours:
        p = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * p, True)

        if len(approx) == 4:
            target = approx
            break
    A = approx[0]
    B = approx[1]
    C = approx[2]
    D = approx[3]

    X = []
    Y = []

    for i in approx:
        X.append(i[0][0])
        Y.append(i[0][1])
    # mapping target points to 800x800 quadrilateral
    width = int(max(math.dist(A[0], B[0]), math.dist(C[0], D[0])))
    height = int(max(math.dist(B[0], C[0]), math.dist(D[0], A[0])))

    approx = rectify(target)
    pts2 = np.float32([[0,height], [0,0],[width,0], [width,height]])

    M = cv2.getPerspectiveTransform(approx,pts2)
    dst = cv2.warpPerspective(orig,M,(width,height))
    dst = cv2.rotate(dst, cv2.ROTATE_90_CLOCKWISE)

    cv2.drawContours(image, [target], -1, (0, 0, 0), 5)

    # using thresholding on warped image to get scanned effect (If Required)
    ret,th1 = cv2.threshold(dst,127,255,cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(dst,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                cv2.THRESH_BINARY,11,2)
    th3 = cv2.adaptiveThreshold(dst,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,11,2)
    ret2,th4 = cv2.threshold(dst,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return dst, th4
cv2.waitKey(0)
cv2.destroyAllWindows()


