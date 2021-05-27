import os
import cv2
import tensorflow as tf
from brain.processing import DisplayProcessor


class Backtester:
    """
    Loads and processes display images for improvement / debugging purposes.
    """
    def __init__(self, input_path):
        self.model = tf.keras.models.load_model('../models/digits_nn')
        self.display_processor = DisplayProcessor()
        self.input_path = input_path

    def run(self):
        file_names = os.listdir(self.input_path)
        for file_name in file_names:
            image = cv2.imread(self.input_path+file_name)
            digits = self.display_processor.extract_digits(image)
            self._validate_digits(digits)

    @staticmethod
    def _validate_digits(digits):
        return True


if __name__ == "__main__":
    disk_path = "D:\\alu-robo\\pi2\\"
    backtester = Backtester(input_path=disk_path)
    backtester.run()