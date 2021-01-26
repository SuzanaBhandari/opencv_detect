from cv2 import cv2 
import numpy as np
import pyautogui


cap = cv2.VideoCapture(0)
lower_blue= np.array([100,150,0])
upper_blue = np.array([140,255,255])



def _get_movement_limit():  
    MVLIMIT = 5
    return MVLIMIT

prev_y = 0
prev_x = 0

#creating a loop forever for video 
while True:

    #gives frame while doing video
    ret, frame = cap.read()

    #creating a mask
    #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #for huesaturation , converting to the huw saturation
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    #for capturing the range that we needed we do masking process
    
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    #for noise reduction proces , using Contours
    
    # Contours can be explained simply as a curve joining all the continuous points (along the boundary), having same color or intensity. The contours are a useful tool for shape analysis and object detection and recognition.
    controus,hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #drawing something,passing frame where we want draw, 
    #-1 indicates                                                                                    

    
    for c in controus:
        area = cv2.contourArea(c)

        if area > 300:
            
            #finding the bounding rectangle 
           
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x , y), (x + w, y + h), (0 , 255 , 0) , 2)
            center_x = x + 0.5*w
            center_y = y + 0.5*h
            # cv2.drawContours(frame,controus,-1,(255,0,0), 2)
            dx = abs(center_x - prev_x)
            dy = abs(center_y - prev_y)

            if dy > _get_movement_limit():
                if center_y > prev_y:
                    pyautogui.press('down')
                    print(y)
                else:
                    pyautogui.press('up')
            prev_y = center_y

            if dx > _get_movement_limit():
                if center_x > prev_x:
                    pyautogui.press('right')
                    
                else:
                    pyautogui.press('left')
            prev_x = center_x

            
            # pyautogui.click(center_x, center_y)
           

    #displaying frames
    cv2.imshow('frame', frame)

    # cv2.imshow('mask', mask)



    #while done with video stoping so for ending, if someone press 'q' stop the video
    if cv2.waitKey(10) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

#Detecting objects in webcam
