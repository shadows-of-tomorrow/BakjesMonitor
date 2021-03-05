import picamera
import numpy as np

class Camera:
    
    def __init__(self, resolution=(512, 512)):
        self.resolution = resolution
        
    def capture(self):
        res = self.resolution
        with picamera.PiCamera() as camera:
            camera.resolution = res
            img = np.empty((res[1], res[0], 3), dtype=np.uint8)
            camera.capture(img, 'bgr')
            return img
            
        