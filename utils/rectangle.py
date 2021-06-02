import json
import cv2


class RectangleHelper:

    def __init__(self, camera):
        self.camera = camera
        self.window_name = "Draw Contours"
        self.config_path = './config/config.json'
        self._set_offsets()
        self.rectangles = []

    def run(self):
        self.rectangles = []
        self._draw_rectangles()
        self._store_rectangles()
        return self.rectangles

    def _set_offsets(self):
        config = self._load_config()
        self.top_offset = config["rectangle_helper"]["top_offset"]
        self.bottom_offset = config["rectangle_helper"]["bottom_offset"]

    def _load_config(self):
        with open(self.config_path, 'r') as file:
            return json.load(file)

    def _store_rectangles(self):
        config = self._load_config()
        config["display_processor"]["RECTANGLES"] = self.rectangles
        with open(self.config_path, 'w') as file:
            json.dump(config, file, indent=4, sort_keys=True)

    def _draw_rectangles(self):

        self.img = self.camera.capture()
        self.img = self.img[self.top_offset:self.bottom_offset, :]
        self.ix = -1
        self.iy = -1
        self.drawing = False

        cv2.namedWindow(winname=self.window_name)
        cv2.setMouseCallback(self.window_name, self.draw_rectangle)
        cv2.imshow(self.window_name, self.img)

        while True:
            key = cv2.waitKey(10)
            if key != -1:
                break
            if cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1:
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
        self.rectangles.append([self.ix, self.iy+self.top_offset, w, h])
