from src.detector import Detector
from src.sources import (
    RTSPSource,
    VideoFileSource,
    USBCameraSource,
    ImageFolderSource,
    SingleImageSource
)
from src.config import Config

def get_source():
    if Config.APP_MODE == 'VIDEO': return VideoFileSource(Config.SOURCE_PATH)
    elif Config.APP_MODE == 'USB': return USBCameraSource(Config.SOURCE_PATH)
    elif Config.APP_MODE == 'FOLDER': return ImageFolderSource(Config.SOURCE_PATH)
    elif Config.APP_MODE == 'IMAGE': return SingleImageSource(Config.SOURCE_PATH)
    elif Config.APP_MODE == 'RTSP': return RTSPSource(Config.get_rtsp_url())
    else: raise ValueError(f"Unknown mode: {Config.APP_MODE}")

def main():
    detector = Detector()
    source = get_source()
    frame_rate = int(source.get_frame_rate())
    batch = []
    try:
        while True:
            ret, frame = source.get_frame()
            if not ret:
                break
            batch.append(frame)
            if len(batch) == frame_rate: # Check license plates in one second
                license = detector.process_batch(batch)
                batch.clear()
                print(license)
    except KeyboardInterrupt:
        print('Stopped by user')
    finally:
        source.release()

if __name__ == "__main__":
    main()
