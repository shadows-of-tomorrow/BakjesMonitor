import time
from switch import Switch
from camera import Camera
from utils import construct_knn_model
from utils import monitor_display


class Engine:

    def __init__(self):
        self.looping = True
        self.lanes = ['top_left', 'top_right']
        self.counters = self._construct_counters()
        self.knn = construct_knn_model()
        self.switch = Switch()
        self.camera = Camera()
        self.step_time = 0.25
        self.wait_time = 8.00
        self.stop_steps = 6

    def _construct_counters(self):
        counters = {}
        for lane in self.lanes:
            counters[lane] = 0
        return counters

    def _get_digits(self):
        display = self.camera.capture()
        digits = monitor_display(self.knn, display)
        print(digits)
        return digits

    def _update_counters(self, digits_old, digits_new):
        for lane in self.lanes:
            if digits_new[lane] == digits_old[lane]:
                self.counters[lane] += 1
                print("Lane <" + str(lane) + "> frozen for " + str(self.counters[lane] * self.step_time) + "seconds.")
            else:
                self.counters[lane] = 0

    def _check_if_stop(self):
        for lane in self.lanes:
            if self.counters[lane] >= self.stop_steps:
                return True
        return False

    def _reset_machine(self):
        print("Turn alarm on!")
        self.switch.turn_on()
        time.sleep(0.1)
        print("Wait for " + str(self.wait_time) + " seconds.")
        time.sleep(self.wait_time)
        print("Turn alarm off!")
        time.sleep(0.1)
        self.switch.turn_off()

    def _reset_counters(self):
        for key in self.counters.keys():
            self.counters[key] = 0

    def run(self):
        self.switch.turn_off()
        digits_old = self._get_digits()
        while self.looping:
            if not self.looping:
                self._reset_counters()
                break
            time.sleep(self.step_time)
            try:
                digits_new = self._get_digits()
                self._update_counters(digits_old, digits_new)
                if self._check_if_stop():
                    self._reset_machine()
                    self._reset_counters()
                digits_old = digits_new
            except Exception as e:
                print("Could not read digits from screen..")
                self._reset_counters()
                time.sleep(1.0)


if __name__ == "__main__":
    engine = Engine()
    engine.run()
