import cv2
from ultralytics import YOLO
from datetime import datetime, timedelta
from config import SHOW_CAMERA, RTSP_URL, MODEL_PATH, WINDOW_NAME, FRAME_WIDTH, TARGET_CLASSES, START_TIME, END_TIME, COOLDOWN_PERIOD, SCREENSHOT_PATH
from utils import preprocess, is_within_time_range, send_notification_alarm, get_detection_color

def run_detection():
    # Load model
    model = YOLO(MODEL_PATH)

    # Initialize OpenCV window
    cv2.namedWindow(WINDOW_NAME)

    # Initialize video capture
    cap = cv2.VideoCapture(RTSP_URL)

    if not cap.isOpened():
        raise IOError(f"Cannot open video stream with RTSP URL: {RTSP_URL}")

    last_detection_time = datetime.min
    detection_frames = []

    while True:
        # Clear buffer by reading frames until the latest one
        for _ in range(5):
            cap.grab()

        ret, frame = cap.retrieve()
        if not ret:
            print("Failed to retrieve frame. Exiting...")
            break

        frame = preprocess(frame, FRAME_WIDTH)

        # Perform object detection
        results = model(frame, verbose=False)
        current_time = datetime.now()

        # Create a copy of the frame to draw detections on
        frame_with_detections = frame.copy()

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = box.cls[0]
                confidence = box.conf[0]
                name = model.names[int(label)]
                color = get_detection_color()

                if name in TARGET_CLASSES:

                    # Draw bounding box and labels
                    cv2.rectangle(frame_with_detections, (x1, y1), (x2, y2), color, 2)

                    # Draw filled rectangle for text background
                    text = f"{name} {confidence:.2%}"
                    (text_width, _text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    cv2.rectangle(frame_with_detections, (x1, y1 - 20), (x1 + text_width, y1), color, -1)

                    # Draw text label
                    cv2.putText(frame_with_detections, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

                    if is_within_time_range(current_time, START_TIME, END_TIME):
                        if current_time - last_detection_time >= timedelta(seconds=COOLDOWN_PERIOD):
                            detection_frames.append(frame_with_detections.copy())
                            last_detection_time = current_time

        # Save screenshots and trigger alarm
        if detection_frames:
            send_notification_alarm(detection_frames, current_time, SCREENSHOT_PATH)
            detection_frames = []  # Reset detection frames after saving

        if SHOW_CAMERA:
            # Display the frame with detections
            cv2.imshow(WINDOW_NAME, frame_with_detections)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
