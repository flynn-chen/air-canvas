#!/usr/bin/env python3

import numpy as np
import keyboard 
import cv2 
import time
from collections import deque 
  
   
# default called trackbar function  
def setValues(x): 
   print("") 
   
# background captured parameters
isBgCaptured = False
bgSubThreshold = 50
learningRate = 0.005

# Creating the trackbars needed for  
# adjusting the marker colour These  
# trackbars will be used for setting  
# the upper and lower ranges of the 
# HSV required for particular colour 
cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors", 
                   144, 180, setValues) 
cv2.createTrackbar("Upper Saturation", "Color detectors", 
                   255, 255, setValues) 
cv2.createTrackbar("Upper Value", "Color detectors",  
                   224, 255, setValues) 
cv2.createTrackbar("Lower Hue", "Color detectors", 
                   45, 180, setValues) 
cv2.createTrackbar("Lower Saturation", "Color detectors",  
                   45, 255, setValues) 
cv2.createTrackbar("Lower Value", "Color detectors",  
                   45, 255, setValues) 
  
  
# Giving different arrays to handle colour 
# points of different colour These arrays  
# will hold the points of a particular colour 
# in the array which will further be used 
# to draw on canvas 
bpoints = [deque(maxlen = 1024)] 
gpoints = [deque(maxlen = 1024)] 
rpoints = [deque(maxlen = 1024)] 
ypoints = [deque(maxlen = 1024)] 

last_blue_index = set()
last_green_index = set()
last_red_index = set()
last_yellow_index = set()
   
# These indexes will be used to mark position 
# of pointers in colour array 
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0
   
# The kernel to be used for dilation purpose  
kernel = np.ones((5, 5), np.uint8) 
  
# The colours which will be used as ink for 
# the drawing purpose 
colors = [(255, 0, 0), (0, 255, 0),  
          (0, 0, 255), (0, 255, 255)] 
colorIndex = 0
   
# Here is code for Canvas setup 
# paintWindow = np.zeros((471, 636, 3)) + 255
   
# cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE) 
   
  
# Loading the default webcam of PC. 
cap = cv2.VideoCapture(0) 
cap.set(3, 640)
cap.set(4, 480)

def removeBG(frame):
    fgmask = bgModel.apply(frame,learningRate=learningRate)
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res

def drawPoints(points, colors, this_frame):
    for i in range(len(points)): 
          
        for j in range(len(points[i])): 
              
            for k in range(1, len(points[i][j])): 
                  
                if points[i][j][k - 1] is None or points[i][j][k] is None: 
                    continue

                cv2.line(this_frame, points[i][j][k - 1], points[i][j][k], colors[i], 2) 
                #cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2) 

def drawBoardPoints(points, this_frame):
    for i in range(len(points)): 
          
        for j in range(len(points[i])): 
              
            for k in range(1, len(points[i][j])): 
                  
                if points[i][j][k - 1] is None or points[i][j][k] is None: 
                    continue
                
                cv2.line(this_frame, points[i][j][k - 1], points[i][j][k], (255, 255, 255), 2) 
                #cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2) 

iteration = 0
   
# Keep looping 
while True: 
      
    # Reading the frame from the camera 
    ret, frame = cap.read()
    if ret == False:
        print("failed to utilize default camera 0")
        exit(1)
      
    # Flipping the frame to see same side of yours 
    frame = cv2.flip(frame, 1) 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   
    # Getting the updated positions of the trackbar 
    # and setting the HSV values 
    u_hue = cv2.getTrackbarPos("Upper Hue", 
                               "Color detectors") 
    u_saturation = cv2.getTrackbarPos("Upper Saturation", 
                                      "Color detectors") 
    u_value = cv2.getTrackbarPos("Upper Value", 
                                 "Color detectors") 
    l_hue = cv2.getTrackbarPos("Lower Hue", 
                               "Color detectors") 
    l_saturation = cv2.getTrackbarPos("Lower Saturation", 
                                      "Color detectors") 
    l_value = cv2.getTrackbarPos("Lower Value", 
                                 "Color detectors") 
    Upper_hsv = np.array([u_hue, u_saturation, u_value]) 
    Lower_hsv = np.array([l_hue, l_saturation, l_value])
   
   
    # Adding the colour buttons to the live frame  
    # for colour access 
    frame = cv2.rectangle(frame, (40, 1), (140, 25),  
                          (122, 122, 122), -1) 
    frame = cv2.rectangle(frame, (160, 1), (255, 25), 
                          colors[0], -1) 
    frame = cv2.rectangle(frame, (275, 1), (370, 25),  
                          colors[1], -1) 
    frame = cv2.rectangle(frame, (390, 1), (485, 25),  
                          colors[2], -1) 
    frame = cv2.rectangle(frame, (505, 1), (600, 25), 
                          colors[3], -1) 
      
    cv2.putText(frame, "CLEAR", (45, 15), 
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, 
                (255, 255, 255), 2, cv2.LINE_AA) 
      
    cv2.putText(frame, "BLUE", (165, 15), 
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, 
                (255, 255, 255), 2, cv2.LINE_AA) 
      
    cv2.putText(frame, "GREEN", (280, 15), 
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, 
                (255, 255, 255), 2, cv2.LINE_AA) 
      
    cv2.putText(frame, "RED", (395, 15), 
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,  
                (255, 255, 255), 2, cv2.LINE_AA) 
      
    cv2.putText(frame, "YELLOW", (510, 15), 
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,  
                (150, 150, 150), 2, cv2.LINE_AA) 
   
   
    # Identifying the pointer by making its  
    # mask 
    if isBgCaptured == True:
        foreground = removeBG(hsv).copy()
        Mask = cv2.inRange(foreground, Lower_hsv, Upper_hsv)
    else:
        Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
    Mask = cv2.erode(Mask, kernel, iterations = 1) 
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel) 
    Mask = cv2.dilate(Mask, kernel, iterations = 1) 
   
    # Find contours for the pointer after  
    # idetifying it 
    cnts, _ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_SIMPLE)
    center = None
   
    # Ifthe contours are formed 
    if len(cnts) > 0 and keyboard.is_pressed(" "): 
          
        # sorting the contours to find biggest  
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0] 
          
        # Get the radius of the enclosing circle  
        # around the found contour 
        ((x, y), radius) = cv2.minEnclosingCircle(cnt) 
          
        # Draw the circle around the contour 
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2) 
        
        # Calculating the center of the detected contour 
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])) 
   
        # Now checking if the user wants to click on  
        # any button above the screen
        if center[1] <= 25: 
              
            # Clear Button 
            if (40 <= center[0] <= 140):  
                bpoints = [deque(maxlen = 512)] 
                gpoints = [deque(maxlen = 512)] 
                rpoints = [deque(maxlen = 512)] 
                ypoints = [deque(maxlen = 512)] 
   
                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0
   
                #paintWindow[67:, :, :] = 255
            elif 160 <= center[0] <= 255: 
                    colorIndex = 0 # Blue 
            elif 275 <= center[0] <= 370: 
                    colorIndex = 1 # Green 
            elif 390 <= center[0] <= 485: 
                    colorIndex = 2 # Red 
            elif 505 <= center[0] <= 600: 
                    colorIndex = 3 # Yellow 
        else : 


            last_blue_index.add(blue_index)
            last_green_index.add(green_index)
            last_red_index.add(red_index)
            last_yellow_index.add(yellow_index)
            if colorIndex == 0: 
                bpoints[blue_index].appendleft(center) 
            elif colorIndex == 1: 
                gpoints[green_index].appendleft(center) 
            elif colorIndex == 2: 
                rpoints[red_index].appendleft(center) 
            elif colorIndex == 3: 
                ypoints[yellow_index].appendleft(center) 
                  
    # Append the next deques when nothing is  
    # detected to avois messing up 
    else: 
        if bpoints[-1] != deque(maxlen = 512):
            bpoints.append(deque(maxlen = 512)) 
            blue_index += 1

        if gpoints[-1] != deque(maxlen = 512):
            gpoints.append(deque(maxlen = 512)) 
            green_index += 1

        if rpoints[-1] != deque(maxlen = 512):
            rpoints.append(deque(maxlen = 512)) 
            red_index += 1

        if ypoints[-1] != deque(maxlen = 512):
            ypoints.append(deque(maxlen = 512)) 
            yellow_index += 1
   
    # Draw lines of all the colors on the 
    # canvas and frame  
    points = [bpoints, gpoints, rpoints, ypoints]
    drawPoints(points, colors, frame)

    # Show all the windows 
    cv2.imshow("Tracking", frame)
    #cv2.imshow("Paint", paintWindow) 
    #cv2.imshow("mask", Mask) 
   
    # Keyboard OP
    k = cv2.waitKey(10)
    if k == 27 or k == ord('q'):  # press ESC to exit
        cap.release()
        cv2.destroyAllWindows()
        break
    elif k == ord('1'): 
        colorIndex = 0 # Blue 
    elif k == ord('2'): 
        colorIndex = 1 # Green 
    elif k == ord('3'): 
        colorIndex = 2 # Red 
    elif k == ord('4'): 
        colorIndex = 3 # Yellow 
    elif k == ord('c'):  # press c to clear
        bpoints = [deque(maxlen = 512)] 
        gpoints = [deque(maxlen = 512)] 
        rpoints = [deque(maxlen = 512)] 
        ypoints = [deque(maxlen = 512)] 

        blue_index = 0
        green_index = 0
        red_index = 0
        yellow_index = 0
    elif k == ord('b') or iteration % 1000 == 2:  # press 'b' to capture the background
        bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
        isBgCaptured = True
        print('Background Captured')
    elif k == ord('s'):  # press 's' to save the screen
        board = np.zeros([frame.shape[0], frame.shape[1]], np.uint8)  # initialize white board
        drawBoardPoints(points, board)
        cv2.imshow("board", board)
        filename = time.strftime("%Y-%m-%d-%H-%M-%S") + ".jpg"
        cv2.imwrite(filename, board)
        print('Screen Shot Taken ' + filename)
    elif k == ord('z'):  # press 's' to save the screen
        try:
            if colorIndex == 0: 
                bpoints.pop(max(last_blue_index))
                last_blue_index.remove(max(last_blue_index))
                blue_index -= 1
            elif colorIndex == 1: 
                gpoints.pop(max(last_green_index))
                last_green_index.remove(max(last_green_index))
                green_index -= 1
            elif colorIndex == 2: 
                rpoints.pop(max(last_red_index))
                last_red_index.remove(max(last_red_index))
                red_index -= 1
            elif colorIndex == 3: 
                ypoints.pop(max(last_yellow_index)) 
                last_yellow_index.remove(max(last_yellow_index))
                yellow_index -= 1
        except:
            pass
        print('Return One Stroke')

    iteration += 1
  
