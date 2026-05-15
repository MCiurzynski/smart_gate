from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    YOLO_PATH = os.environ.get('YOLO_PATH')
    LICENSE_PLATE_OCR = os.environ.get('LICENSE_PLATE_OCR')