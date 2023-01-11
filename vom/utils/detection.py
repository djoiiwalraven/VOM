import cv2
import numpy as np

extractor = cv2.createBackgroundSubtractorMOG2()

def motion(image,dis=False):
    
    # Neccesserry to add stabilization algorithm below:
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # CALCULATING IMAGE MOVEMENT
    AVG = np.empty(image.shape)
    #blur = cv2.GaussianBlur(image, (11, 11), 3)
    blur = image
    
    cv2.accumulateWeighted(blur, AVG, 0.5)
    res1 = cv2.convertScaleAbs(AVG)
    fg_mask = extractor.apply(AVG)
    #fg_mask = cv2.GaussianBlur(fg_mask, (5, 5), 10)

    # RESULTS
    #motion_image = cv2.bitwise_and(image, image, mask=fg_mask)
    if dis: cv2.imshow('fg',edges(fg_mask))
    #if dis: cv2.imshow('fg',fg_mask)
    return edges(fg_mask)

def edges(image):
    # BLUR BEFORE EDGE DETECTION NEEDED
    image = cv2.GaussianBlur(image, (11, 11), 3)
    return cv2.Canny(image, 250,255)

def calculate_motion(frame):
    return cv2.countNonZero(frame)
