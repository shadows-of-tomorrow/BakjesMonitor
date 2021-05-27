import os
import cv2


class DummyCamera:

    def __init__(self, input_path, resolution=(512, 512)):
        self.input_path = input_path
        self.resolution = resolution
        self.image_names = os.listdir(self.input_path)
        self.img_idx = 0

    def capture(self):
        image = cv2.imread(self.input_path + self.image_names[self.img_idx])
        image = cv2.resize(image, self.resolution)
        self.img_idx += 1
        return image
