import cv2 as cv
import numpy as np
import mediapipe as mp
import pyautogui as ptg
from collections import deque
import time





SMOOTHING_FACTOR = 5
BLINK_THRESHOLD = 0.003
CLICK_DELAY = 0.1
DOUBLE_BLINK_THRESHOLD = 0.5
RIGHT_CLICK_DURATION = 0.4  # Duration for right-click detection
SCROLL_SENSITIVITY = 10  # Pixels to trigger scroll

# Initialize the camera and face mesh
cam = cv.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_width, screen_height = ptg.size()

# Queue to store previous positions for smoothing
previous_positions = deque(maxlen=SMOOTHING_FACTOR)
previous_y = None  # Store previous Y position for scroll detection


# Variables for gesture detection
last_blink_time = 0
blink_count = 0
right_eye_close_start = 0
is_right_eye_closed = False
left_eye_partial_close_start = 0
is_scrolling = False

while True:
    _, frame = cam.read()
    frame = cv.flip(frame, 1)
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_point = output.multi_face_landmarks
    frame_height, frame_width, _ = frame.shape

    if landmark_point:
        landmarks = landmark_point[0].landmark
        
        # Eye tracking for cursor movement
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


        # Eye state detection
        left = [landmarks[145], landmarks[159]]
        right = [landmarks[374], landmarks[386]]
        
        left_blink = (left[0].y - left[1].y) < BLINK_THRESHOLD
        right_blink = (right[0].y - right[1].y) < BLINK_THRESHOLD


        left_partial = (left[0].y - left[1].y) < BLINK_THRESHOLD * 2  # Partial blink threshold

        # Draw eye indicators
        for landmark in left + right:
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            cv.circle(frame, (x, y), 3, (0, 100, 250))


        # Right-click detection
        if right_blink and not is_right_eye_closed:
            right_eye_close_start = time.time()
            is_right_eye_closed = True
        elif not right_blink and is_right_eye_closed:
            if time.time() - right_eye_close_start > RIGHT_CLICK_DURATION:
                ptg.rightClick()
                ptg.sleep(CLICK_DELAY)
            is_right_eye_closed = False

        # Scroll functionality
        if left_partial and not is_scrolling:
            is_scrolling = True
            previous_y = screen_y
        elif left_partial and is_scrolling and previous_y is not None:
            y_diff = screen_y - previous_y
            if abs(y_diff) > SCROLL_SENSITIVITY:
                scroll_amount = int(y_diff // SCROLL_SENSITIVITY)
                ptg.scroll(-scroll_amount)  # Negative for natural scrolling
                previous_y = screen_y
        elif not left_partial:
            is_scrolling = False
            previous_y = None

        # Regular left click
        if left_blink and not right_blink and not is_scrolling:
            ptg.click()
            ptg.sleep(CLICK_DELAY)

        # Double blink detection for exit
        if left_blink and right_blink:
            current_time = time.time()
            if current_time - last_blink_time < DOUBLE_BLINK_THRESHOLD:
                blink_count += 1
                if blink_count >= 2:


                    break
            else:
                blink_count = 1
            last_blink_time = current_time






    cv.imshow('Eye Controlled Mouse', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv.destroyAllWindows()