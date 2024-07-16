# CFTV - Computer Vision

This project is a computer vision system for monitoring RTSP streams, detecting objects of interest (e.g., persons, cars), and saving screenshots of detections. The system can run in the background without displaying the camera feed, and it supports configurable settings through environment variables.

## Features

- Detects objects of interest from an RTSP stream using YOLOv8.
- Saves screenshots of detections with bounding boxes and labels.
- Optionally displays the camera feed in a window.
- Configurable detection targets, time range, and cooldown period.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/victorkl400/cftv-opencv.git
   cd cftv-opencv
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your `.env` file:

   ```plaintext
   RTSP_URL=your_rtsp_url
   MODEL_PATH=yolov8l.pt
   TARGET_CLASSES=person,car
   FRAME_WIDTH=640
   SCREENSHOT_PATH=screenshots
   START_TIME=08:00
   END_TIME=12:00
   COOLDOWN_PERIOD=30
   WINDOW_NAME=CFTV - Computer Vision
   SHOW_CAMERA=true
   ```

## Configuration

- `RTSP_URL`: URL of the RTSP stream.
- `MODEL_PATH`: Path to the YOLOv8 model.
- `TARGET_CLASSES`: Comma-separated list of target classes to detect (e.g., `person,car`).
- `FRAME_WIDTH`: Width of the frame to resize for processing.
- `SCREENSHOT_PATH`: Directory to save screenshots.
- `START_TIME`: Start time for detection (HH:MM).
- `END_TIME`: End time for detection (HH:MM).
- `COOLDOWN_PERIOD`: Cooldown period between detections in seconds.
- `WINDOW_NAME`: Name of the window if `SHOW_CAMERA` is true.
- `SHOW_CAMERA`: Boolean to show the camera feed window (`true` or `false`).

## Usage

Run the detection system with the following command:

```bash
python main.py
```

If `SHOW_CAMERA` is set to true in the .env file, the camera feed will be displayed in a window. If set to false, the system will run in the background without displaying the feed.

## Files

- config.py: Loads configuration from environment variables.
- detection.py: Contains the main detection loop and drawing functions.
- main.py: Entry point to run the application.
- utils.py: Contains utility functions for preprocessing, time checking, random color generation, and managing trackers.
