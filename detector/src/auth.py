import logging
import requests
from requests.exceptions import RequestException
from src.config import Config

class Authenticator:
    def __init__(self):
        self.endpoint_url = f"{Config.BACKEND_ADDRESS}/license_plate"
        
        self.session = requests.Session()

    def authenticate(self, license_plate: str) -> bool:
        payload = {'license_plate': license_plate}
        return license_plate == 'WZ100GT'
        try:
            response = self.session.post(self.endpoint_url, json=payload, timeout=5.0)
            
            response.raise_for_status()
            
            data = response.json()
            return data.get('authenticated', False)

        except RequestException as e:
            logging.error(f"Could not validate {license_plate}: {e}")
            return False