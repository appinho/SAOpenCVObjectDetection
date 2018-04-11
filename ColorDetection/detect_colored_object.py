# import libraries
import cv2
import numpy as np

# define empty method for trackbar
def nothing(x):
    pass

# capture video
cap = cv2.VideoCapture(0)

# set up trackbar
trackbar = np.zeros((200,560,3), np.uint8)
cv2.namedWindow('Parameter')
cv2.createTrackbar('Hue min','Parameter',0,255,nothing)
cv2.createTrackbar('Sat min','Parameter',0,255,nothing)
cv2.createTrackbar('Val min','Parameter',0,255,nothing)
cv2.createTrackbar('Hue max','Parameter',0,255,nothing)
cv2.createTrackbar('Sat max','Parameter',0,255,nothing)
cv2.createTrackbar('Val max','Parameter',0,255,nothing)
cv2.createTrackbar('Erode kernel size','Parameter',0,20,nothing)
cv2.createTrackbar('Dilate kernel size','Parameter',0,20,nothing)
switch = '1'
cv2.createTrackbar(switch, 'Parameter',0,1,nothing)

while(True):
    
    # capture current image
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # read parameters
    h_min = cv2.getTrackbarPos('Hue min','Parameter')
    s_min = cv2.getTrackbarPos('Sat min','Parameter')
    v_min = cv2.getTrackbarPos('Val min','Parameter')
    h_max = cv2.getTrackbarPos('Hue max','Parameter')
    s_max = cv2.getTrackbarPos('Sat max','Parameter')
    v_max = cv2.getTrackbarPos('Val max','Parameter')
    swi = cv2.getTrackbarPos(switch,'Parameter')
    erode_kernel_size =  cv2.getTrackbarPos('Erode kernel size','Parameter')
    erode_kernel = np.ones((erode_kernel_size,erode_kernel_size),np.uint8)
    #erode_kernel = np.ones((5,5),np.uint8)
    dilate_kernel_size =  cv2.getTrackbarPos('Dilate kernel size','Parameter')
    dilate_kernel = np.ones((dilate_kernel_size,dilate_kernel_size),np.uint8)
    #dilate_kernel = np.ones((13,13),np.uint8)
    if swi == 0:
        trackbar[:] = 0
    else:
        trackbar[:] = (np.array([h_min,s_min,v_min])+np.array([h_max,s_max,v_max]))/2
        trackbar = cv2.cvtColor(trackbar, cv2.COLOR_HSV2BGR)

    # filter color
    lower_color = np.array([h_min,s_min,v_min])
    #lower_color = np.array([30,65,160])
    upper_color = np.array([h_max,s_max,v_max])
    #upper_color = np.array([100,125,220])
    bin_color_img = cv2.inRange(hsv, lower_color, upper_color)
    #filtered = cv2.bitwise_and(frame,frame, mask= bin_color_img)

    # erode image
    bin_erode_img = cv2.erode(bin_color_img,erode_kernel)

    # dilate image
    bin_dilate_img = cv2.dilate(bin_erode_img,dilate_kernel)

    # find contours
    contour_image, contours, hierarchy = cv2.findContours(bin_dilate_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # fit bounding box
    try: hierarchy = hierarchy[0]
    except: hierarchy = []

    height, width = bin_dilate_img.shape
    min_x, min_y = width, height
    max_x = max_y = 0

    output_img = frame.copy()
    for contour, hier in zip(contours, hierarchy):
        (x,y,w,h) = cv2.boundingRect(contour)
        #print(x,y,w,h)
        min_x, max_x = min(x, min_x), max(x+w, max_x)
        min_y, max_y = min(y, min_y), max(y+h, max_y)
        if w > 80 and h > 80:
            cv2.rectangle(output_img, (x,y), (x+w,y+h), (255, 0, 0), 2)

    if max_x - min_x > 0 and max_y - min_y > 0:
        cv2.rectangle(output_img, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)
    
    # display steps
    cv2.imshow('Parameter',trackbar)
    cv2.moveWindow('Parameter',20,0)
    cv2.imshow('Input',frame)
    cv2.moveWindow('Input',620,0)
    cv2.imshow('HSV',hsv)
    cv2.moveWindow('HSV',1250,0)
    cv2.imshow('Mask',bin_color_img)
    cv2.moveWindow('Mask',0,560)
    #cv2.imshow('erode',ero)
    #cv2.moveWindow('erode',0,600)
    cv2.imshow('Morph',bin_dilate_img)
    cv2.moveWindow('Morph',675,560)
    cv2.imshow('Output',output_img)
    cv2.moveWindow('Output',1250,560)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release stream
cap.release()
cv2.destroyAllWindows()
