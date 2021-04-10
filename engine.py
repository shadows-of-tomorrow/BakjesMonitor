import time
from switch import Switch
from camera import Camera
from utils import construct_knn_model
from utils import monitor_display

class Engine:
    
    def __init__(self):
        self.counter = 0
        self.knn = construct_knn_model()
        self.switch = Switch()
        self.camera = Camera()
        self.step_time = 0.25
        self.wait_time = 8.00
        
    def _get_digits(self):
            display = self.camera.capture()
            digits = monitor_display(self.knn, display)
            return digits
        
    def run(self):
        self.switch.turn_off()
        digits_old = self._get_digits()
        while True:
            time.sleep(self.step_time)
            try:
                digits_new = self._get_digits()
                print(digits_new)
                if digits_new['top_left'] == digits_old['top_left'] or digits_new['top_right'] == digits_old['top_right']:
                    self.counter += 1
                    print("Screen frozen for " + str(self.counter * self.step_time) + " seconds.")
                    if self.counter >= 3:
                        print("Turn alarm on!")
                        self.switch.turn_on()
                        time.sleep(0.1)
                        print("Wait for " + str(self.wait_time) + " seconds...")
                        time.sleep(self.wait_time)
                        print("Turn alarm off!")
                        time.sleep(0.1)
                        self.switch.turn_off()
                        self.counter = 0
                else:
                    self.counter = 0
                digits_old = digits_new
            except:
                print("Could not read digits from screen..")
                time.sleep(1.0)
            
        
if __name__ == "__main__":
    engine = Engine()
    engine.run()
        