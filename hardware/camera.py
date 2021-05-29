import picamera
import numpy as np


class Camera:

    def __init__(self, resolution=(512, 512)):
        self.resolution = resolution
        self.camera = self._initialize_camera()

    def _initialize_camera(self):
        camera = picamera.PiCamera(resolution=self.resolution, framerate=90)
        return camera

    def capture(self):
        with self.camera as camera:
            img = np.empty((self.resolution[1], self.resolution[0], 3), dtype=np.uint8)
            camera.capture(img, 'bgr')
            return img
