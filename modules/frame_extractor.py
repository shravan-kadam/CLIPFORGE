import cv2
import os

OUTPUT_DIR = "assets/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_frame(video_path):
    cap = cv2.VideoCapture(video_path)

    success, frame = cap.read()
    cap.release()

    if not success:
        raise ValueError("Could not read frame from video.")

    frame_path = os.path.join(OUTPUT_DIR, "frame.jpg")
    cv2.imwrite(frame_path, frame)

    return frame_path
