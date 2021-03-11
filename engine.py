import cv2
from camera import Camera
from utils import construct_knn_model
from utils import monitor_display

class Engine:
    
    def __init__(self):
        self.counter = 1
        self.knn = construct_knn_model()
        self.camera = Camera()
        
    def _get_digits(self):
            display = self.camera.capture()
            cv2.imwrite('display.png', display)
            digits = monitor_display(self.knn, display)
            print(digits)
        
    def run(self):
        while True:
            self._get_digits()
            self.counter += 1
        
        
if __name__ == "__main__":
    engine = Engine()
    engine.run()
        