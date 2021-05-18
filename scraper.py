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
        while True:
            time.sleep(self.wait_interval)
            try:
                display = self.camera.capture()
                image_path = f"{self.data_path}/{time.time() * 1000}.png"
                print(f"Writing {image_path} to disk...")
                cv2.imwrite(image_path , display)
            except Exception as e:
                print(f"Failed: {e}")


if __name__ == "__main__":
    drive_path = ""
    scraper = Scraper(data_path=drive_path)
    scraper.run()
