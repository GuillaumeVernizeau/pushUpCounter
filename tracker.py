#!/usr/bin/env python3
import cv2
import mediapipe as mp

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Initialize video capture from camera (set the source to a video file path for video input)
cap = cv2.VideoCapture(0)

pushup = 0
below_line = False

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and get the pose landmarks
    results = pose.process(frame_rgb)

    # Draw the pose landmarks on the frame
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Get the coordinates of the left and right elbows and the corners of the mouth
        left_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
        right_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
        mouth_left = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT]
        mouth_right = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_RIGHT]

        # Calculate the approximate center of the mouth
        mouth_center_x = (mouth_left.x + mouth_right.x) / 2
        mouth_center_y = (mouth_left.y + mouth_right.y) / 2

        # Convert the normalized coordinates to pixel coordinates
        left_elbow_x, left_elbow_y = int(
            left_elbow.x * frame.shape[1]), int(left_elbow.y * frame.shape[0])
        right_elbow_x, right_elbow_y = int(
            right_elbow.x * frame.shape[1]), int(right_elbow.y * frame.shape[0])
        mouth_x, mouth_y = int(
            mouth_center_x * frame.shape[1]), int(mouth_center_y * frame.shape[0])

        # Draw a red line connecting the two elbows
        cv2.line(frame, (left_elbow_x, left_elbow_y),
                 (right_elbow_x, right_elbow_y), (0, 0, 255), 2)

        # Calculate the Y-coordinate of the line at the mouth's X-coordinate
        line_slope = (right_elbow_y - left_elbow_y) / \
            (right_elbow_x - left_elbow_x)
        line_y = left_elbow_y + line_slope * (mouth_x - left_elbow_x)

        # Check if the mouth is below the line
        if mouth_y > line_y:
            below_line = True
        elif below_line:
            pushup += 1
            below_line = False
            print(f'Pushup count: {pushup}')

    # Display the frame
    cv2.imshow('Body Tracker', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
