import cv2 as cv
import numpy as np


cap = cv.VideoCapture(0)

while(True):

    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # define range of blue color in HSV

    # upper and lower bounds for red color
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # upper and lower bounds for green color
    lower_green = np.array([40, 40, 40])  
    upper_green = np.array([90, 255, 255])

    # Threshold the HSV image to get only blue colors

    # Create a red mask
    mask1 = cv.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv.inRange(hsv, lower_red2, upper_red2)
    
    # Bitwise-OR the masks
    maskRed = mask1 | mask2

    # Create a green mask
    maskGreen = cv.inRange(hsv, lower_green, upper_green)
    #
    mask = maskRed + maskGreen

    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)

    # Count the number of red and green pixels
    red_pixels = cv.countNonZero(maskRed)
    green_pixels = cv.countNonZero(maskGreen)

    # Print the color with more pixels
    if (red_pixels > green_pixels):
        print( "Red")
    else:
        print( "Green")

    # Show the images
    cv.imshow('frame',frame)
    cv.imshow('mask',mask)
    cv.imshow('res',res)

    # press q to close the window
    if cv.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
