import time
from switch import Switch
from camera import Camera
from utils import construct_knn_model
from utils import monitor_display


class Engine:

    def __init__(self):
        self.lanes = ['top_left', 'top_right']
        self.switch_id = 'switch_1'
        self.counters = self._construct_counters()
        self.knn = construct_knn_model()
        self.switch = Switch(self.switch_id)
        self.camera = Camera()
        self.wait_time = 8.00
        self.step_time = 0.30
        self.stop_steps = 4
        self.digits_old = {'top_left': 0, 'top_right': 0, 'bottom_left': 0, 'bottom_right': 0}
        self.digits_new = {'top_left': 0, 'top_right': 0, 'bottom_left': 0, 'bottom_right': 0}
        self.looping = True
        self.alarm_on = False

    def reset_switch(self, switch_id):
        self.switch_id = switch_id
        self.switch = Switch(switch_id)

    def _construct_counters(self):
        counters = {}
        for lane in self.lanes:
            counters[lane] = 0
        return counters

    def _get_digits(self):
        display = self.camera.capture()
        digits = monitor_display(self.knn, display)
        return digits

    def _update_counters(self, digits_old, digits_new):
        for lane in self.lanes:
            if digits_new[lane] == digits_old[lane]:
                self.counters[lane] += 1
            else:
                self.counters[lane] = 0

    def _check_if_stop(self):
        for lane in self.lanes:
            if self.counters[lane] >= self.stop_steps:
                return True
        return False

    def _reset_machine(self):
        self.switch.turn_on()
        self.alarm_on = True
        time.sleep(self.wait_time)
        self.switch.turn_off()
        self.alarm_on = False

    def _reset_counters(self):
        for key in self.counters.keys():
            self.counters[key] = 0

    def run(self):
        self.switch.turn_off()
        self.digits_old = self._get_digits()
        while self.looping:
            if not self.looping:
                self._reset_counters()
                break
            time.sleep(self.step_time)
            try:
                self.digits_new = self._get_digits()
                self._update_counters(self.digits_old, self.digits_new)
                if self._check_if_stop():
                    self._reset_machine()
                    self._reset_counters()
                self.digits_old = self.digits_new
            except Exception as e:
                self._reset_counters()


if __name__ == "__main__":
    engine = Engine()
    engine.run()
