import time
import json
import os
from hardware.alarm import Alarm
from hardware.camera import Camera
from .processing import DisplayProcessor


class Engine:

    def __init__(self):
        self.config = self._load_config()
        self.lanes = self.config["lanes"]
        self.alarm_time = self.config["alarm_time"]
        self.step_time = self.config["step_time"]
        self.stop_steps = self.config["stop_steps"]
        self.digits_old = {'top_left': 0, 'top_right': 0, 'bottom_left': 0, 'bottom_right': 0}
        self.digits_new = {'top_left': 0, 'top_right': 0, 'bottom_left': 0, 'bottom_right': 0}
        self.looping = True
        self.alarm_on = False
        self.counters = self._construct_counters()
        self.alarm = Alarm()
        self.camera = Camera()
        self.display_processor = DisplayProcessor()

    def run(self):
        self.alarm.turn_off()
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

    def _construct_counters(self):
        counters = {}
        for lane in self.lanes:
            counters[lane] = 0
        return counters

    def _get_digits(self):
        display = self.camera.capture()
        digits = self.display_processor.extract_digits(display)
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
        self.alarm.turn_on()
        self.alarm_on = True
        time.sleep(self.alarm_time)
        self.alarm.turn_off()
        self.alarm_on = False

    def _reset_counters(self):
        for key in self.counters.keys():
            self.counters[key] = 0

    def _load_config(self):
        config_path = self._get_config_path()
        with open(config_path, 'r') as file:
            return json.load(file)['engine']

    def _get_config_path(self):
        dir_path = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(dir_path, 'config', 'config.json')
