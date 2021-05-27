import os
import cv2
import csv
import numpy as np


class Cleaner:
    """
    Transforms raw image files into a csv for model training purposes.
    """
    def __init__(self, input_path, output_path):
        self.size = (28, 28)
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        images_list = self._construct_images_list()
        self._write_images_list(images_list)

    def _write_images_list(self, images_list):
        with open(self.output_path + 'digits.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(images_list)

    def _construct_images_list(self):
        images_list = []
        dir_names = os.listdir(self.input_path)
        for dir_name in dir_names:
            file_names = os.listdir(self.input_path + dir_name)
            for file_name in file_names:
                image = cv2.imread(self.input_path + dir_name + "/" + file_name, cv2.IMREAD_GRAYSCALE)
                image = self._process_image(image)
                image_list = self._image_to_list(image, int(dir_name))
                images_list.append(image_list)
        return images_list

    def _image_to_list(self, image, digit):
        image_flat = list(image.flatten())
        return [digit] + image_flat

    def _process_image(self, image):
        image = 255 - image
        image_trim = self._trim_edges(image)
        image_shap = cv2.resize(image_trim, self.size)
        image_shap = 255 - image_shap
        return image_shap

    def _trim_edges(self, image):
        filled_cols = np.sum(image, axis=0) != 0.0
        image_trim = image[:, filled_cols]
        filled_rows = np.sum(image, axis=1) != 0.0
        image_trim = image_trim[filled_rows, :]
        return image_trim


if __name__ == "__main__":
    png128_path = "D:/alu-robo/digits/png128/"
    csv28_path = "D:/alu-robo/digits/csv28/"
    processor = Cleaner(input_path=png128_path, output_path=csv28_path)
    processor.run()
