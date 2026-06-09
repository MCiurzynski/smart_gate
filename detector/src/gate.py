import requests
from src.config import Config

class Gate:
    def open(self):
        try:
            response = requests.get(Config.GATE_URL, timeout=3)
            if response.status_code == 200:
                print("Sygnał wysłany. Odpowiedź ESP:", response.text, flush=True)
            else:
                print(f"Błąd HTTP: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Błąd połączenia z ESP32: {e}")