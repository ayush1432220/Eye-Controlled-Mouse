import cv2 as cv
import numpy as np
import mediapipe as mp
import pyautogui as ptg


cam = cv.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_width,screen_height = ptg.size()
 
while True:
    _, frame = cam.read()
    frame = cv.flip(frame,1)
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    lankmark_point = output.multi_face_landmarks
    frame_height,frame_width, _ = frame.shape
    if lankmark_point:
        landmarks = lankmark_point[0].landmark
        for id, landmark in enumerate (landmarks[474:478]):
            x = int(landmark.x * frame_width)
            y = int(landmark.y *frame_height)
            cv.circle(frame,(x,y),3,(0,100,100))
            if id ==1:
                screen_x = screen_width / frame_width * x
                screen_y = screen_height / frame_height *y
                ptg.moveTo(x,y)
        left = [landmarks[145],landmarks[159]]
        for landmark in left:
             x = int(landmark.x * frame_width)
             y = int(landmark.y *frame_height)
             cv.circle(frame,(x,y),3,(0,100,250))
        if(left[0].y-left[1].y)<0.004:
            ptg.click()
            ptg.sleep(1)
    cv.imshow('Eye Controlled Mous',frame)
    cv.waitKey(1) 