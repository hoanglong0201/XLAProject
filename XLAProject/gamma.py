import cv2
import numpy as np

def Gamma(img,g):
	img = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)
	a = np.float32(img)/255
	imgnew = np.uint8(np.power(a,g)*255)
	return imgnew