import logging
import requests
from requests.exceptions import RequestException
from src.config import Config

class Authenticator:
    def __init__(self):
        
        self.session = requests.Session()

    def authenticate(self, license_plate: str) -> bool:
        try:
            response = self.session.get(f'{Config.BACKEND_URL}/plates/{license_plate}', timeout=5.0)
            
            return response.ok

        except RequestException as e:
            logging.error(f"Could not validate {license_plate}: {e}")
            return False