from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    YOLO_PATH = os.environ.get('YOLO_PATH')
    LICENSE_PLATE_OCR = os.environ.get('LICENSE_PLATE_OCR')
    APP_MODE = os.environ.get('APP_MODE')
    SOURCE_PATH = os.environ.get('SOURCE_PATH')
    CAMERA_USER = os.environ.get('CAMERA_USER')
    CAMERA_PASSWORD = os.environ.get('CAMERA_PASSWORD')
    CAMERA_IP = os.environ.get('CAMERA_IP')
    CAMERA_PORT = os.environ.get('CAMERA_PORT')
    RTSP_PATH = os.environ.get('RTSP_PATH')
    BATCH_SIZE = int(os.environ.get('BATCH_SIZE'))

    # Backend API base URL the detector reports detections to.
    BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8000/api')

    REGION_CONF = 0.9
    CHARS_CONF = 0.9

    BACKEND_ADDRESS=os.environ.get('BACKEND_ADDRESS')

    @staticmethod
    def get_rtsp_url() -> str:
        return f"rtsp://{Config.CAMERA_USER}:{Config.CAMERA_PASSWORD}@{Config.CAMERA_IP}:{Config.CAMERA_PORT}/{Config.RTSP_PATH}"