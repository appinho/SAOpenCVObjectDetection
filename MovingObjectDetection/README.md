# opencv_moving_object_detection
Python Code to detect a moving object with OpenCV 3.2.0 library

# Dependencies:
OpenCV 3.2.0,
Python 2.7,
Numpy Library,

# Workflow:
  1. Read avi video
  2. Capture current image and calculate absolute differrence to the last one         (Top left image)                         
  3. Convert result into a binary image                                               (Top right image)
  4. Blur image with dilation filter or blur smoothing to enhance white pixel areas
  5. Convert result again into a binary image                                         (Bottom left image)
  6. Find contours and fit rectangle around detection                                 (Bottom right image)

# Example:
![](example.png)

# Alternative
A C++ solution can be found here: https://www.youtube.com/watch?v=X6rPdRZzgjg
