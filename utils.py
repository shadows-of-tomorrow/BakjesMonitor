import cv2
import numpy as np

REL_WIDTH_LOW = 1.25
REL_WIDTH_HIGH = 3
DIST_THRESHOLD = 350
DIGIT_SHAPE = (30, 50)
MIN_CONTOUR_AREA = 150
MAX_PIXEL_VALUE = 255.0
CLUSTER_THRESHOLD = 20.0


def monitor_display(knn_model, display):
    digits_raw = find_digits(knn_model, display)
    digits_clean = sort_and_group_digits(digits_raw)
    return digits_clean


def find_digits(knn_model, image):
    digits = []
    image_thresh = threshold_image(image)
    contours = find_contours(image_thresh)
    for cnt in contours:
        cnt_area = cv2.contourArea(cnt)
        if cnt_area > MIN_CONTOUR_AREA:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if REL_WIDTH_LOW < h / w <= REL_WIDTH_HIGH:
                roi = image_thresh[y:y + h, x:x + w]
                roi_small = cv2.resize(roi, DIGIT_SHAPE)
                roi_small = threshold_image(roi_small)
                roi_small = roi_small.reshape((1, int(DIGIT_SHAPE[0] * DIGIT_SHAPE[1]))) / MAX_PIXEL_VALUE
                roi_small = np.float32(roi_small)
                _, results, _, dists = knn_model.findNearest(roi_small, k=1)
                if dists[0][0] <= DIST_THRESHOLD:
                    digits.append((results[0][0], x, y))
    return digits


def sort_and_group_digits(digits):
    xs = [digit[1] for digit in digits]
    ys = [digit[2] for digit in digits]
    tl, tr, bl, br = find_corner_idxs(xs, ys)
    digits_tl = group_digits_around_idx(digits, tl)
    digits_tr = group_digits_around_idx(digits, tr)
    digits_bl = group_digits_around_idx(digits, bl)
    digits_br = group_digits_around_idx(digits, br)
    digits_grouped = {
        'top_left': digits_tl,
        'top_right': digits_tr,
        'bottom_left': digits_bl,
        'bottom_right': digits_br
    }
    return digits_grouped


def group_digits_around_idx(digits, idx):
    digit_ref = digits[idx]
    digits_subset = [digit for digit in digits if
                     np.abs(digit[1] - digit_ref[1]) + np.abs(digit[2] - digit_ref[2]) < CLUSTER_THRESHOLD]
    if len(digits_subset) > 1:
        digits_subset = sorted(digits_subset, key=lambda digit: -digit[1])
    digits_subset = int(np.sum([digits_subset[k][0] * (10.0 ** k) for k in range(len(digits_subset))]))
    return digits_subset


def find_corner_idxs(xs, ys):
    tl = find_top_left_idx(xs, ys)
    bl = find_bottom_left_idx(xs, ys)
    tr = find_top_right_idx(xs, ys)
    br = find_bottom_right_idx(xs, ys)
    return tl, tr, bl, br


def find_top_left_idx(xs, ys):
    return np.argmin([xs[k] + ys[k] for k in range(len(xs))])


def find_bottom_left_idx(xs, ys):
    max_y = np.max(ys)
    return np.argmin([xs[k] + max_y - ys[k] for k in range(len(xs))])


def find_top_right_idx(xs, ys):
    max_x = np.max(xs)
    return np.argmin([max_x - xs[k] + ys[k] for k in range(len(xs))])


def find_bottom_right_idx(xs, ys):
    return np.argmax([xs[k] + ys[k] for k in range(len(xs))])


def construct_knn_model():
    x_digits = np.loadtxt('./data/digits_x.data', np.float32) / MAX_PIXEL_VALUE
    y_digits = np.loadtxt('./data/digits_y.data', np.float32)
    y_digits = y_digits.reshape((y_digits.size, 1))
    knn_model = cv2.ml.KNearest_create()
    knn_model.train(x_digits, cv2.ml.ROW_SAMPLE, y_digits)
    return knn_model


def threshold_image(image):
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (5, 5), 0)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return image


def find_contours(image):
    contours, _ = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours
