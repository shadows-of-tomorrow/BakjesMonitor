import time
import numpy as np
import tensorflow as tf


class TFTimer:

    def __init__(self, n_iterations=10):
        self.n_iterations = n_iterations
        self.digit_clf = self._load_digit_classifier()
        self.digit_clf_lite = self._load_lite_digit_classifier()

    def run(self):
        x_dummy = self._create_dummy_matrix()
        self._time_lite_model(x_dummy)
        self._time_h5_model(x_dummy)

    def _time_h5_model(self, x_dummy):
        for k in range(self.n_iterations):
            start = time.time()
            self.digit_clf(x_dummy)
            end = time.time()
            print(f"h5 model pt {k} took {round(end - start, 7)}s")

    def _time_lite_model(self, x_dummy):
        for k in range(self.n_iterations):
            start = time.time()
            self._call_lite_model(x_dummy)
            end = time.time()
            print(f"Lite model pt {k} took {round(end - start, 7)}s")

    def _call_lite_model(self, x_dummy):
        input_details = self.digit_clf_lite.get_input_details()
        output_details = self.digit_clf_lite.get_output_details()
        self.digit_clf_lite.set_tensor(input_details[0]['index'], x_dummy)
        self.digit_clf_lite.invoke()
        output_data = self.digit_clf_lite.get_tensor(output_details[0]['index'])
        return output_data

    def _load_lite_digit_classifier(self):
        interpreter = tf.lite.Interpreter("../models/digits_nn_lite.tflite")
        interpreter.allocate_tensors()
        return interpreter

    @staticmethod
    def _create_dummy_matrix():
        return np.random.normal(loc=0.0, scale=1.0, size=(1, 28, 28, 1)).astype('float32')

    @staticmethod
    def _load_digit_classifier():
        return tf.keras.models.load_model('../models/digits_nn')


if __name__ == "__main__":
    TFTimer().run()
