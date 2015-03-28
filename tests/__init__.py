import os
import unittest

from PIL import Image

FILES_PATH = 'files'
IMAGE_PATH = os.path.join(FILES_PATH, 'images')
IMAGE_FILENAME = 'floating.jpg'
WM_PNG_FILENAME = 'wiki-2.png'
WM_JPG_FILENAME = 'logo.jpg'
BUILD_FOLDER = os.path.join(FILES_PATH, 'build')


class WaterMarkUnitTestBase(unittest.TestCase):

    def get_image_filename(self):
        return IMAGE_FILENAME

    def get_base_dir(self):
        return os.path.dirname(__file__)

    def get_image_file(self):
        base_dir = self.get_base_dir()
        image_file = os.path.join(base_dir, IMAGE_PATH, IMAGE_FILENAME)
        return image_file

    def get_watermark_png_with_alpha_file(self):
        base_dir = self.get_base_dir()
        image_file = os.path.join(base_dir, IMAGE_PATH, WM_PNG_FILENAME)
        return image_file

    def get_watermark_jpg_file(self):
        base_dir = self.get_base_dir()
        image_file = os.path.join(base_dir, IMAGE_PATH, WM_JPG_FILENAME)
        return image_file

    def get_output_dir(self):
        base_dir = self.get_base_dir()
        return os.path.join(base_dir, BUILD_FOLDER)

    def check_image_file(self, img_path):
        im = Image.open(img_path)
        assert im.filename == img_path
        im.close()

    def remove_file(self, file_path):
        os.remove(file_path)


class WaterMarkIntegrationTestBase(unittest.TestCase):
    pass
