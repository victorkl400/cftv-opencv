import cv2
import random
import os
from datetime import datetime

def print_current_time():
    print(datetime.now())

def preprocess(img, target_width):
    """Resize the image maintaining the aspect ratio."""
    height, width = img.shape[:2]
    ratio = height / width
    img = cv2.resize(img, (target_width, int(target_width * ratio)))
    return img

def is_within_time_range(current_time, start_time, end_time):
    """Check if the current time is within the specified time range."""
    return start_time <= current_time.time() <= end_time

def send_notification_alarm(detection_frames, current_time, screenshot_path):
    """Function to handle notification alarm and other actions."""
    print(f"Detected objects at {current_time.strftime('%H:%M:%S')}")
    for detection in detection_frames:
        screenshot_file = os.path.join(screenshot_path, f"screenshot_{current_time.strftime('%Y%m%d_%H%M%S')}.jpg")
        cv2.imwrite(screenshot_file, detection)  # Save the last frame with all detections

def get_detection_color():
    """Get a color."""
    return [0,51,255]
