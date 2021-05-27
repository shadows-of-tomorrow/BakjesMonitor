import cv2
import json
from hardware.camera import Camera
from brain.processing import DisplayProcessor


class CropHelper:

    def __init__(self):
        self.camera = Camera()
        self.display_processor = DisplayProcessor()
        self.store_config = False

    def run(self):
        while not self.store_config:
            self._modify_crop_config()
            self._show_display()
            self._prompt_config_store()

    def _prompt_config_store(self):
        self.store_config = str(input("Store crop settings?")).lower() == 'yes'
        if self.store_config:
            with open('./config/config.json', 'r') as file:
                config = json.load(file)
            config["display_processor"]["ROTATION_DEGREES"] = self.display_processor.rotation_degrees
            config["display_processor"]["CROP_BOTTOM_PIXELS"] = self.display_processor.crop_bottom_pixels
            config["display_processor"]["CROP_TOP_PIXELS"] = self.display_processor.crop_top_pixels
            config["display_processor"]["CROP_RIGHT_PIXELS"] = self.display_processor.crop_right_pixels
            config["display_processor"]["CROP_LEFT_PIXELS"] = self.display_processor.crop_left_pixels
            config["display_processor"]["WHITE_STRIP_RIGHT"] = self.display_processor.white_strip_right
            config["display_processor"]["WHITE_STRIP_LEFT"] = self.display_processor.white_strip_left
            with open('./config/config.json', 'w') as file:
                json.dump(config, file, indent=4, sort_keys=True)

    def _modify_crop_config(self):
        print("-"*50)
        self.display_processor.rotation_degrees = int(input("Degrees of display rotation (0 for none)"))
        self.display_processor.crop_bottom_pixels = int(input("Crop pixels at bottom (1 for none)"))
        self.display_processor.crop_top_pixels = int(input("Pixels cropped from top edge (0 for none)"))
        self.display_processor.crop_right_pixels = int(input("Pixels cropped from right edge (1 for none)"))
        self.display_processor.crop_left_pixels = int(input("Pixels cropped from left edge (0 for none)"))
        self.display_processor.white_strip_right = int(input("Pixels whitened right from center (0 for none)"))
        self.display_processor.white_strip_left = int(input("Pixels whitened left from center (0 for none)"))

    def _show_display(self):
        display = self.camera.capture()
        display = self.display_processor._preprocess_display(display)
        cv2.imshow('display', display)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
