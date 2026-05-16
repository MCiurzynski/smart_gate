from fast_plate_ocr import LicensePlateRecognizer
from ultralytics import YOLO
from src.config import Config
from collections import Counter
import re

class Detector:
    def __init__(self):
        self.yolo_model = YOLO(Config.YOLO_PATH)
        self.ocr_model = LicensePlateRecognizer(Config.LICENSE_PLATE_OCR)
        self.validator = LicensePlateValidator()

    def process_batch(self, frames):
        """Processes frames batch and returns set of detected license plate"""
        results = self.yolo_model.predict(frames, verbose=False)
        license_plates = []
        counter = Counter()
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy.cpu()[0])
                license = r.orig_img[y1:y2, x1:x2]
                license_plates.append(license)
        if len(license_plates) > 0:
            ocr_results = self.ocr_model.run(license_plates, return_confidence=True)
            plates = [o.plate for o in ocr_results 
                      if o.region is not None
                      and o.region_prob > Config.REGION_CONF
                      and (o.char_probs > Config.CHARS_CONF).all()]
            counter.update(plates)
        plates = set(counter)
        return self.validator.validate_plates(plates)
    
class LicensePlateValidator:
    def __init__(self):
        self._one_char = r'^([A-Z])([A-Z0-9]{3})$'
        self._one_char_vehicle = [
            r'^\d{3}$',
            r'^\d{2}[A-Z]$',
            r'^[1-9][A-Z][1-9]$',
            r'^[A-Z]\d{2}$',
            r'^[1-9][A-Z]{2}$',
            r'^[A-Z]{2}[1-9]$',
            r'^[A-Z][1-9][A-Z]$'
        ]
        self._two_char = r'^([A-Z]{2})([A-Z0-9]{5})$'
        self._two_char_vehicle = [
            r'^\d{5}$',
            r'^\d{4}[A-Z]$',
            r'^\d{3}[A-Z]{2}$',
            r'^[1-9][A-Z]\d{3}$',
            r'^[1-9][A-Z]{2}\d{2}$'
        ]
        self._three_char = r'^([A-Z]{3})([A-Z0-9]{4,5})$'
        self._three_char_vehicle = [
            r'^[A-Z]\d{3}$',
            r'^\d{2}[A-Z]{2}$',
            r'^[1-9][A-Z]\d{2}$',
            r'^\d{2}[A-Z][1-9]$',
            r'^[1-9][A-Z]{2}[1-9]$',
            r'^[A-Z]{2}\d{2}$',
            r'^\d{5}$',
            r'^\d{4}[A-Z]$',
            r'^\d{3}[A-Z]{2}$',
            r'^[A-Z]\d{2}[A-Z]$',
            r'^[A-Z][1-9][A-Z]{2}$',
            r'^\d{3}[A-Z]{2}$'
        ]

    def validate_plates(self, plates):
        valid_plates = []
        for plate in plates:
            if self._validate_plate(plate):
                valid_plates.append(plate)
        return set(valid_plates)
    
    def _validate_plate(self, plate):
        if self._validate_1_char(plate):
            return True
        elif self._validate_2_char(plate):
            return True
        elif self._validate_3_char(plate):
            return True
        return False
    
    def _validate_1_char(self, plate):
        m = re.match(self._one_char, plate)
        if m:
            vehicle = m.group(2)
            for reg in self._one_char_vehicle:
                if re.match(reg, vehicle):
                    return True
            return False
        else:
            return False
    
    def _validate_2_char(self, plate):
        m = re.match(self._two_char, plate)
        if m:
            vehicle = m.group(2)
            for reg in self._two_char_vehicle:
                if re.match(reg, vehicle):
                    return True
            return False
        else:
            return False
        
    def _validate_3_char(self, plate):
        m = re.match(self._three_char, plate)
        if m:
            vehicle = m.group(2)
            for reg in self._three_char_vehicle:
                if re.match(reg, vehicle):
                    return True
            return False
        else:
            return False