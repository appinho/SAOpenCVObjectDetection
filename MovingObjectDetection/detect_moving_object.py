# Import libraries
import cv2
import numpy as np
from time import sleep

# Method to obtain next frame and check if end of the video is reached
def get_frame(FRAME_COUNTER):
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    FRAME_COUNTER +=1
    if FRAME_COUNTER == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        FRAME_COUNTER = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    return frame, FRAME_COUNTER

# Access video
cap = cv2.VideoCapture('bouncingBall.avi')

# Init parameters
FRAME_COUNTER = 0
BINARY_THRESHOLD = 30       # threshold for binarizing 3 channel 8 bit image to 1 channel 8 bit image
BLURRING_METHOD = True      # if true use dilation, if false use blur smoothing
DILATION_KERNEL_SIZE = 15
BLUR_KERNEL_SIZE = 30
DELAY = 0.1                 # artificial DELAY of the played video in milliseconds

# First image captured outside the loop for initial comparision
frame_recent,FRAME_COUNTER = get_frame(FRAME_COUNTER)

# Continuously play video
while(True):
    # Save image from last frame
    frame_last = frame_recent
    
    # Obtain new frame
    frame_recent,FRAME_COUNTER = get_frame(FRAME_COUNTER)

    # Calculate difference of both frames and binarize result
    diff = cv2.absdiff(frame_recent,frame_last)
    ret,thresh1 = cv2.threshold(diff,BINARY_THRESHOLD,255,cv2.THRESH_BINARY)

    # Dilation or blur smoothing to enhance white pixel areas in image
    if(BLURRING_METHOD):
        dilate_kernel = np.ones((DILATION_KERNEL_SIZE,DILATION_KERNEL_SIZE),np.uint8)
        blurred = cv2.dilate(thresh1,dilate_kernel)
    else:
        blurred = cv2.blur(thresh1,(BLUR_KERNEL_SIZE,BLUR_KERNEL_SIZE))

    # Binarize result again
    ret,thresh2 = cv2.threshold(blurred,30,255,cv2.THRESH_BINARY)

    # Find contours
    contour_image, contours, hierarchy = cv2.findContours(thresh2, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # Fit bounding box
    try: hierarchy = hierarchy[0]
    except: hierarchy = []
    height, width = thresh2.shape
    min_x, min_y = width, height
    max_x = max_y = 0

    # Convert input frame to visualize output
    output_img = cv2.cvtColor(frame_recent, cv2.COLOR_GRAY2BGR)

    # Display all found contours via rectangles
    for contour, hier in zip(contours, hierarchy):
        (x,y,w,h) = cv2.boundingRect(contour)
        min_x, max_x = min(x, min_x), max(x+w, max_x)
        min_y, max_y = min(y, min_y), max(y+h, max_y)
        if w > 80 and h > 80:
            cv2.rectangle(output_img, (x,y), (x+w,y+h), (255, 0, 0), 2)
        if max_x - min_x > 0 and max_y - min_y > 0:
            cv2.rectangle(output_img, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)
    
    # Display the resulting frame
    #cv2.imshow('Difference',diff)
    #cv2.imshow('First threshold',thresh1)
    #cv2.imshow('Second threshold',thresh2)
    cv2.imshow('Output',output_img)

    sleep(DELAY)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
