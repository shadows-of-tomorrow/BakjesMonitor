import time
import cv2
from camera import Camera


class Scraper:
    """
    Collects and stores a stream of images for model improvement purposes.
    """

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.camera = Camera()
        self.wait_interval = 0.20

    def run(self):
        time.sleep(self.wait_interval)
        display = self.camera.capture()
        cv2.imwrite(f"{self.data_path}\\{time.time() * 1000}.png", display)


if __name__ == "__main__":
    drive_path = ""
    scraper = Scraper(data_path=drive_path)
    scraper.run()
