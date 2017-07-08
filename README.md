# opencv_color_object_detection
Python Code to detect a colored object with OpenCV 3.2.0 library

Dependencies: OpenCV 3.2.0, Python 2.7, Numpy Library

Code pipelin:
  1. Create VideoCapture object
  2. Create Trackbar to adjust parameters
  3. Loop through consecutive images of webcam stream
  4. Capture current image
  5. Read parameters
  6. Filter the HSV image with upper and lower HSV values
  7. Erode white pixels
  8. Dilate white pixels
  9. Find contours and fit rectangle around detection
  10. Display each step
  11. Release VideoCapture object
