import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Constants
WINDOW_NAME = os.getenv("WINDOW_NAME", "CFTV - Computer Vision")
RTSP_URL = os.getenv("RTSP_URL")
MODEL_PATH = os.getenv("MODEL_PATH", "yolov8l.pt")
TARGET_CLASSES = os.getenv("TARGET_CLASSES", "person").split(',')
FRAME_WIDTH = int(os.getenv("FRAME_WIDTH", "640"))
SCREENSHOT_PATH = os.getenv("SCREENSHOT_PATH", "screenshots")
SHOW_CAMERA =(os.getenv("SHOW_CAMERA") == 'true')
os.makedirs(SCREENSHOT_PATH, exist_ok=True)

COOLDOWN_PERIOD = int(os.getenv("COOLDOWN_PERIOD", "30"))

START_TIME = datetime.strptime(os.getenv("START_TIME", "00:00"), "%H:%M").time()
END_TIME = datetime.strptime(os.getenv("END_TIME", "23:58"), "%H:%M").time()
