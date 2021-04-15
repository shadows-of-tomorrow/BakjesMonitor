import random
import time


class DummyEngine:

    def __init__(self):
        self.looping = False
        self.lanes = ['top_left']
        self.allowed_digits = [k for k in range(51)]
        self.wait_time = 8.00
        self.step_time = 0.25
        self.stop_steps = 6
        self.alarm_on = False
        self.digits_old = {'top_left': 0, 'top_right': 0, 'bottom_left': 0, 'bottom_right': 0}

    def reset_switch(self, switch_id):
        print(switch_id)

    def run(self):
        while self.looping:
            time.sleep(self.step_time)
            self.digits_old = self._get_digits()
            if not self.looping:
                break

    def _get_digits(self):
        return {
            'top_left': random.choices(self.allowed_digits)[0],
            'top_right': random.choices(self.allowed_digits)[0],
            'bottom_left': random.choices(self.allowed_digits)[0],
            'bottom_right': random.choices(self.allowed_digits)[0]
        }
