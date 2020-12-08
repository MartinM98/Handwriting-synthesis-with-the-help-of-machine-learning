import unittest
import cv2
from src.file_handler.file_handler import get_absolute_path
from src.image_processing.resize import resize_image, combine, crop_image


class ImageProcessingIntegrationTests(unittest.TestCase):
    """
    The class tests methods from image processing functions.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('\n[START]  Image Processing Integration Tests')

    @classmethod
    def tearDownClass(cls):
        """ after all tests """
        print('\n[END]    Image Processing Integration Tests')

    @classmethod
    def setUp(cls):
        """ before each test """

    def test_integration_image(self):
        pass

    def test_resize_image(self):
        path_to_image = get_absolute_path(
            './tests/data/letter.png')
        self.assertIsNotNone(path_to_image)
        result = resize_image(path_to_image, 256, 256)
        self.assertTrue(result.shape == (256, 256, 3))

    def test_combine(self):
        path_to_image = get_absolute_path(
            './tests/data/letter.png')
        self.assertIsNotNone(path_to_image)
        result = combine(path_to_image, path_to_image)
        self.assertTrue(result.shape == (33, 84, 3))

    def test_crop_image(self):
        path_to_image = get_absolute_path(
            './tests/data/letter_resized.png')
        output_path = get_absolute_path(
            './tests/data/cropped.png')
        self.assertIsNotNone(path_to_image)
        crop_image(path_to_image, output_path)
        result = cv2.imread(output_path)
        self.assertTrue(result.shape[0] < 256)
        self.assertTrue(result.shape[1] < 256)


if __name__ == '__main__':
    unittest.main()
