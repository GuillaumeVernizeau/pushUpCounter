#!/usr/bin/env python3
import cv2
import mediapipe as mp


class PushupDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose()
        self.pushup_count = 0
        self.below_line = False

    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame_rgb, self.pose.process(frame_rgb)

    def draw_landmarks(self, frame, landmarks):
        self.mp_drawing.draw_landmarks(
            frame, landmarks, self.mp_pose.POSE_CONNECTIONS)

    def update_pushup_count(self, frame, landmarks):
        left_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW]
        right_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
        mouth_left = landmarks.landmark[self.mp_pose.PoseLandmark.MOUTH_LEFT]
        mouth_right = landmarks.landmark[self.mp_pose.PoseLandmark.MOUTH_RIGHT]

        mouth_center_x = (mouth_left.x + mouth_right.x) / 2
        mouth_center_y = (mouth_left.y + mouth_right.y) / 2

        left_elbow_x, left_elbow_y = int(
            left_elbow.x * frame.shape[1]), int(left_elbow.y * frame.shape[0])
        right_elbow_x, right_elbow_y = int(
            right_elbow.x * frame.shape[1]), int(right_elbow.y * frame.shape[0])
        mouth_x, mouth_y = int(
            mouth_center_x * frame.shape[1]), int(mouth_center_y * frame.shape[0])

        line_slope = (right_elbow_y - left_elbow_y) / \
            (right_elbow_x - left_elbow_x)
        line_y = left_elbow_y + line_slope * (mouth_x - left_elbow_x)

        if mouth_y > line_y:
            self.below_line = True
        elif self.below_line:
            self.pushup_count += 1
            self.below_line = False
            print(f'Pushup count: {self.pushup_count}')

    def reset_pushup_count(self):
        self.pushup_count = 0

    def display_pushup_count(self, frame):
        cv2.putText(frame, f'Pushup count: {self.pushup_count}', (
            10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    def are_landmarks_visible(self, landmarks):
        required_landmarks = [
            self.mp_pose.PoseLandmark.LEFT_ELBOW,
            self.mp_pose.PoseLandmark.RIGHT_ELBOW,
            self.mp_pose.PoseLandmark.MOUTH_LEFT,
            self.mp_pose.PoseLandmark.MOUTH_RIGHT
        ]

        return all(landmarks.landmark[lm].visibility > 0.5 for lm in required_landmarks)

    def display_landmark_warning(self, frame):
        message = "Elbows and mouth must be visible"
        text_size = cv2.getTextSize(
            message, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        x = int((frame.shape[1] - text_size[0]) / 2)
        y = int(frame.shape[0] / 2)
        cv2.putText(frame, message, (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)


def main():
    detector = PushupDetector()
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb, results = detector.process_frame(frame)
        if results.pose_landmarks:
            if detector.are_landmarks_visible(results.pose_landmarks):
                detector.draw_landmarks(frame, results.pose_landmarks)
                detector.update_pushup_count(frame, results.pose_landmarks)
                detector.display_pushup_count(frame)
            else:
                detector.display_landmark_warning(frame)
        else:
            detector.display_landmark_warning(frame)

        cv2.imshow('Body Tracker', frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('r'):  # Press 'r' to reset the counter
            detector.reset_pushup_count()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
