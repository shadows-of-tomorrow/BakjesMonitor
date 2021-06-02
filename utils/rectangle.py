import json
import cv2
from hardware.camera import Camera


class RectangleHelper:

    def __init__(self):
        self.camera = Camera()
        self.window_name = "Draw Contours"
        self.config_path = './config/config.json'
        self.rectangles = []

    def run(self):
        self.rectangles = []
        self._draw_rectangles()
        self._store_rectangles()
        return self.rectangles

    def _store_rectangles(self):
        with open(self.config_path, 'r') as file:
            config = json.load(file)
        config["display_processor"]["RECTANGLES"] = self.rectangles
        with open(self.config_path, 'w') as file:
            json.dump(config, file, indent=4, sort_keys=True)

    def _draw_rectangles(self):

        self.base_img = self.camera.capture()
        self.img = self.camera.capture()
        self.ix = -1
        self.iy = -1
        self.drawing = False

        cv2.namedWindow(winname=self.window_name)
        cv2.setMouseCallback(self.window_name, self.draw_rectangle)
        cv2.imshow(self.window_name, self.img)

        while True:
            key = cv2.waitKey(10)
            if key != -1 or cv2.getWindowProperty(self.window_name, 0) == -1:
                break

        cv2.destroyAllWindows()

    def draw_rectangle(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix = x
            self.iy = y

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing == True:
                copy = self.img.copy()
                cv2.rectangle(
                    copy,
                    pt1=(self.ix, self.iy),
                    pt2=(x, y),
                    color=(0, 0, 0),
                    thickness=1
                )
                cv2.imshow(self.window_name, copy)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            cv2.rectangle(
                self.img,
                pt1=(self.ix, self.iy),
                pt2=(x, y),
                color=(0, 255, 0),
                thickness=1
            )
            cv2.imshow(self.window_name, self.img)
            self._store_contour(x, y)

    def _store_contour(self, x, y):
        w = x - self.ix
        h = y - self.iy
        self.rectangles.append([self.ix, self.iy, w, h])
