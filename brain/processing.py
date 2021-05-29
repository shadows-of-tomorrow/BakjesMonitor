import cv2
import json
import time
import scipy.ndimage
import numpy as np
import tensorflow as tf


class DisplayProcessor:

    def __init__(self):
        self.config = self._load_config()
        self.rel_width_low = self.config['REL_WIDTH_LOW']
        self.rel_width_high = self.config['REL_WIDTH_HIGH']
        self.digit_shape = self.config['DIGIT_SHAPE']
        self.min_contour_area = self.config['MIN_CONTOUR_AREA']
        self.max_contour_area = self.config['MAX_CONTOUR_AREA']
        self.cluster_threshold = self.config['CLUSTER_THRESHOLD']
        self.prediction_threshold = self.config['PREDICTION_THRESHOLD']
        self.crop_bottom_pixels = self.config['CROP_BOTTOM_PIXELS']
        self.crop_top_pixels = self.config['CROP_TOP_PIXELS']
        self.crop_right_pixels = self.config['CROP_RIGHT_PIXELS']
        self.crop_left_pixels = self.config['CROP_LEFT_PIXELS']
        self.white_strip_right = self.config['WHITE_STRIP_RIGHT']
        self.white_strip_left = self.config['WHITE_STRIP_LEFT']
        self.rotation_degrees = self.config['ROTATION_DEGREES']
        self.digit_clf = self._load_digit_classifier()

    def extract_digits(self, display):
        digits_raw = self._find_digits(display)
        print(f"Raw digits: {digits_raw}")
        digits_clean = self._sort_and_group_digits(digits_raw)
        print(f"Clean digits: {digits_clean}")
        return digits_clean

    def _call_classifier(self, x):
        input_details = self.digit_clf.get_input_details()
        output_details = self.digit_clf.get_output_details()
        self.digit_clf.set_tensor(input_details[0]['index'], x)
        self.digit_clf.invoke()
        output_data = self.digit_clf.get_tensor(output_details[0]['index'])
        return output_data

    def _find_digits(self, display):
        digits = []
        display = self._preprocess_display(display)
        contours = self._find_contours(display)
        for cnt in contours:
            cnt_area = cv2.contourArea(cnt)
            if self.min_contour_area < cnt_area < self.max_contour_area:
                [x, y, w, h] = cv2.boundingRect(cnt)
                if self.rel_width_low < h / w <= self.rel_width_high:
                    roi = self._extract_roi(display, x, y, w, h)
                    y_clf = self._call_classifier(roi)
                    if np.max(y_clf) >= self.prediction_threshold:
                        digit = np.argmax(y_clf)
                        digits.append([digit, x, y])
        return digits

    def _extract_roi(self, display, x, y, w, h):
        roi = display[y:y + h, x:x + w]
        roi = cv2.resize(roi, (self.digit_shape, self.digit_shape)) / 255.0
        roi = roi.reshape((1, self.digit_shape, self.digit_shape, 1))
        roi = np.float32(roi)
        return roi

    def _sort_and_group_digits(self, digits):
        if len(digits) > 0:
            xs = [digit[1] for digit in digits]
            ys = [digit[2] for digit in digits]
            tl, tr, bl, br = self._find_corner_idxs(xs, ys)
            digits_tl = self._group_digits_around_idx(digits, tl)
            digits_tr = self._group_digits_around_idx(digits, tr)
            digits_bl = self._group_digits_around_idx(digits, bl)
            digits_br = self._group_digits_around_idx(digits, br)
            digits_grouped = {
                'top_left': digits_tl,
                'top_right': digits_tr,
                'bottom_left': digits_bl,
                'bottom_right': digits_br
            }
            return digits_grouped
        else:
            return {
                'top_left': 99,
                'top_right': 99,
                'bottom_left': 99,
                'bottom_right': 99
            }

    def _group_digits_around_idx(self, digits, idx):
        digit_ref = digits[idx]
        l1_dist = [np.abs(digit[1] - digit_ref[1]) + np.abs(digit[2] - digit_ref[2]) for digit in digits]
        digits_subset = [digits[k] for k in range(len(digits)) if l1_dist[k] <= self.cluster_threshold]
        if len(digits_subset) > 1:
            digits_subset = sorted(digits_subset, key=lambda digit: -digit[1])
        digits_subset = int(np.sum([digits_subset[k][0] * (10.0 ** k) for k in range(len(digits_subset))]))
        if digits_subset >= 100:  # Hard coded clipping of excessive index.
            digits_subset = digits_subset // 10
        return digits_subset

    def _find_corner_idxs(self, xs, ys):
        tl = self._find_top_left_idx(xs, ys)
        bl = self._find_bottom_left_idx(xs, ys)
        tr = self._find_top_right_idx(xs, ys)
        br = self._find_bottom_right_idx(xs, ys)
        return tl, tr, bl, br

    @staticmethod
    def _find_top_left_idx(xs, ys):
        return np.argmin([xs[k] + ys[k] for k in range(len(xs))])

    @staticmethod
    def _find_bottom_left_idx(xs, ys):
        max_y = np.max(ys)
        return np.argmin([xs[k] + max_y - ys[k] for k in range(len(xs))])

    @staticmethod
    def _find_top_right_idx(xs, ys):
        max_x = np.max(xs)
        return np.argmin([max_x - xs[k] + ys[k] for k in range(len(xs))])

    @staticmethod
    def _find_bottom_right_idx(xs, ys):
        return np.argmax([xs[k] + ys[k] for k in range(len(xs))])

    def _preprocess_display(self, image):
        image = self._threshold_image(image)
        image = self._crop_image(image)
        image = self._strip_center(image)
        image = self._rotate_image(image)
        return image

    def _rotate_image(self, image):
        if self.rotation_degrees != 0:
            return scipy.ndimage.rotate(image, self.rotation_degrees)
        else:
            return image

    @staticmethod
    def _threshold_image(image):
        if len(image.shape) > 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.GaussianBlur(image, (5, 5), 0)
        image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        return image

    def _strip_center(self, image):
        img_center = int(image.shape[1] / 2)
        image[:, img_center - self.white_strip_left:img_center + self.white_strip_right] = 255.0
        return image

    def _crop_image(self, image):
        image_cropped = image[self.crop_top_pixels:-self.crop_bottom_pixels, self.crop_left_pixels:-self.crop_right_pixels]
        return image_cropped

    @staticmethod
    def _find_contours(image):
        contours, _ = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    @staticmethod
    def _load_config():
        with open('./config/config.json', 'r') as file:
            return json.load(file)['display_processor']

    @staticmethod
    def _load_digit_classifier():
        interpreter = tf.lite.Interpreter("./models/digits_nn_lite.tflite")
        interpreter.allocate_tensors()
        return interpreter
