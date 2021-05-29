import picamera
import numpy as np


class Camera:

    def __init__(self, resolution=(512, 512)):
        self.resolution = resolution
        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.empty_trgt = np.empty((resolution[1], resolution[0], 3), dtype=np.uint8)

    def capture(self):
        img = self.empty_trgt
        self.camera.capture(img, 'bgr')
        return img
