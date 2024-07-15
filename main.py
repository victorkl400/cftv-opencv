import os
import cv2
from ultralytics import YOLO
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
WINDOW_NAME = "CFTV - Computer Vision"
RTSP_URL = os.getenv("RTSP_URL")
MODEL_PATH = "yolov8l.pt"
TARGET_CLASSES = ['person', 'car']
FRAME_WIDTH = 640

# Check if RTSP_URL is set
if not RTSP_URL:
    raise ValueError("RTSP_URL environment variable is not set or is empty.")

# Load model
model = YOLO(MODEL_PATH)

# Initialize OpenCV window
cv2.namedWindow(WINDOW_NAME)

def preprocess(img, target_width=FRAME_WIDTH):
    """Resize the image maintaining the aspect ratio."""
    height, width = img.shape[:2]
    ratio = height / width
    img = cv2.resize(img, (target_width, int(target_width * ratio)))
    return img

# Initialize video capture
cap = cv2.VideoCapture(RTSP_URL)

if not cap.isOpened():
    raise IOError(f"Cannot open video stream with RTSP URL: {RTSP_URL}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to retrieve frame. Exiting...")
        break

    frame = preprocess(frame)
    frame_detected = frame.copy()

    # Perform object detection
    results = model(frame)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = box.cls[0]
            confidence = box.conf[0]
            name = model.names[int(label)]

            if name in TARGET_CLASSES:
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)

                # Draw bounding box and labels
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
                cv2.putText(frame, f"{name} {confidence:.2%}", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

    # Display the frame
    cv2.imshow(WINDOW_NAME, frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
