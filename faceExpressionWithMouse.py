import cv2 as cv
import numpy as np
import mediapipe as mp
import pyautogui as ptg
from collections import deque
import time
import webbrowser 

# counstant Clibration parameters
SMOOTHING_FACTOR = 5
BLINK_THRESHOLD = 0.004
CLICK_DELAY = 0.2
DOUBLE_BLINK_THRESHOLD = 0.3
SMILE_THRESHOLD = 0.01

cam = cv.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
screen_width, screen_height = ptg.size()

previous_positions = deque(maxlen=SMOOTHING_FACTOR)

last_blink_time = 0
blink_count = 0
click_cooldown = 0
smile_detected = False  
double_click_cooldown = 0  
exit_blink_count = 0 

while True:
    _, frame = cam.read()
    if not _:
        print("Failed to grab frame")
        break
    frame = cv.flip(frame, 1)
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_point = output.multi_face_landmarks
    frame_height, frame_width, _ = frame.shape
    current_time = time.time()

    if landmark_point:
        landmarks = landmark_point[0].landmark

        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            cv.circle(frame, (x, y), 3, (0, 100, 100))
            if id == 1:
                screen_x = screen_width * landmark.x
                screen_y = screen_height * landmark.y
                previous_positions.append((screen_x, screen_y))
                avg_x = sum(pos[0] for pos in previous_positions) / len(previous_positions)
                avg_y = sum(pos[1] for pos in previous_positions) / len(previous_positions)
                ptg.moveTo(avg_x, avg_y)

        left = [landmarks[145], landmarks[159]]
        right = [landmarks[374], landmarks[386]]

        left_distance = abs(left[0].y - left[1].y)
        right_distance = abs(right[0].y - right[1].y)

        for landmark in left + right:
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            cv.circle(frame, (x, y), 3, (0, 255, 0) if left_distance < BLINK_THRESHOLD else (0, 100, 250))

        # Single Click Detect krna     
        if left_distance < BLINK_THRESHOLD and current_time - click_cooldown > CLICK_DELAY:
            ptg.click()
            click_cooldown = current_time
            cv.putText(frame, 'Click!', (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Double Click Detect krna
        if left_distance < BLINK_THRESHOLD and right_distance < BLINK_THRESHOLD and current_time - double_click_cooldown > DOUBLE_BLINK_THRESHOLD:
            if current_time - last_blink_time < DOUBLE_BLINK_THRESHOLD:
                ptg.doubleClick()
                double_click_cooldown = current_time + DOUBLE_BLINK_THRESHOLD 
                blink_count = 0 #Reset
            else:
                blink_count = 1
            last_blink_time = current_time

        #Double times Both eyes blink krengey to Exit hoga 
        if left_distance < BLINK_THRESHOLD and right_distance < BLINK_THRESHOLD:
            if current_time - last_blink_time < DOUBLE_BLINK_THRESHOLD:
                exit_blink_count += 1 # increment the counter
                if exit_blink_count >= 2: # Counter Exit krne k liye 
                    break 
            else:
                exit_blink_count = 1 # If Blink fast nhi tha Then counter reset krna hai

            last_blink_time = current_time # update last blink time

        else:
            exit_blink_count = 0  # Reset the exit blink counter if not blinking
        # Smile Detection and Open Chrome
        upper_lip = landmarks[13].y
        lower_lip = landmarks[14].y
        lip_distance = abs(upper_lip - lower_lip)

        if lip_distance > SMILE_THRESHOLD and not smile_detected:
            print("Smile Detected! Opening Chrome.")
            webbrowser.open("https://www.google.com")
            smile_detected = True
            cv.putText(frame, 'Smile!', (50, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        if lip_distance <= SMILE_THRESHOLD:
            smile_detected = False

    cv.imshow('Eye Controlled Mouse', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv.destroyAllWindows()