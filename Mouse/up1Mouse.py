import cv2 as cv
import numpy as np
import mediapipe as mp
import pyautogui as ptg
import time

cam = cv.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_width, screen_height = ptg.size()

last_screen_x, last_screen_y = screen_width // 2, screen_height // 2
last_click_time = 0
double_click_threshold = 0.4  

while True:
    _, frame = cam.read()
    frame = cv.flip(frame, 1)
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_height, frame_width, _ = frame.shape

    current_mouse_x, current_mouse_y = ptg.position()

    if (current_mouse_x != last_screen_x or current_mouse_y != last_screen_y):
        last_screen_x, last_screen_y = current_mouse_x, current_mouse_y

    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            cv.circle(frame, (x, y), 3, (0, 100, 100))
            if id == 1:
                screen_x = screen_width / frame_width * x
                screen_y = screen_height / frame_height * y
                ptg.moveTo(screen_x, screen_y)
                last_screen_x, last_screen_y = screen_x, screen_y 

        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            cv.circle(frame, (x, y), 3, (0, 100, 250))
        if (left[0].y - left[1].y) < 0.004:
            current_time = time.time()
            if (current_time - last_click_time) < double_click_threshold:
                ptg.doubleClick()
            else:
                ptg.click()
            last_click_time = current_time
            ptg.sleep(0.1)
    else:
        ptg.moveTo(last_screen_x, last_screen_y)

    cv.imshow('Eye Controlled Mouse', frame)
    cv.waitKey(1)
