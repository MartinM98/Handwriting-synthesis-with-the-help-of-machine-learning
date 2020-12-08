import unittest
import cv2
from src.file_handler.file_handler import get_absolute_path
from src.image_processing.resize import resize_image, combine, crop_image

from unittest.mock import Mock
from tkinter import filedialog
import numpy as np


# ------------ common_functions.py ------------
from src.image_processing.common_functions.common_functions import get_dir_and_file
from src.image_processing.common_functions.common_functions import get_dir
from src.image_processing.common_functions.common_functions import get_image
from src.image_processing.common_functions.common_functions import prepare_blank_image
from src.image_processing.common_functions.common_functions import resize_and_show_images
from src.image_processing.common_functions.common_functions import get_parts

# ------------ automated_functions.py ------------
from src.image_processing.automated_functions import gabor_filter_automated
from src.image_processing.automated_functions import skeletonize_automated
from src.image_processing.automated_functions import process_dataset

# ------------ binary_search_filter.py ------------
from src.image_processing.binary_search_filter import binary_search_filter

# ------------ gabor_filter.py ------------
from src.image_processing.gabor_filter import gabor_filter

# ------------ skeletonize.py ------------
from src.image_processing.skeletonize import skeletonize_image


class ImageProcessingIntegrationTests(unittest.TestCase):
    """
    The class tests methods from image processing functions.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('\n[START]  Image Processing Integration Tests')
        cls.test_image = prepare_blank_image(shape=(10, 10))
        cls.test_control_points = get_image(
            get_absolute_path('tests/data/control_points.png'))
        cls.parts = []
        get_parts(cls.test_control_points, 3, cls.parts)

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

    # ------------ common_functions.py ------------

    def test_get_dir_and_file(self):
        filedialog.askopenfilename = Mock(return_value='/usr/local/test.png')
        self.assertTupleEqual(get_dir_and_file(),
                              ('/usr/local', 'test', '/usr/local/test.png'))
        filedialog.askopenfilename = Mock(return_value='')
        self.assertTupleEqual(get_dir_and_file(), ('', '', ''))

    def test_get_dir(self):
        filedialog.askdirectory = Mock(return_value='/usr')
        self.assertEqual(get_dir(), '/usr')
        filedialog.askdirectory = Mock(return_value='')
        self.assertEqual(get_dir(), '')
        filedialog.askdirectory = Mock(return_value='/usr/local')
        self.assertEqual(get_dir(), '/usr/local')

    def test_get_image(self):
        self.assertIsNotNone(self.test_control_points)
        self.assertTupleEqual(self.test_control_points.shape, (17, 16))

    def test_prepare_blank_image(self):
        self.assertTupleEqual(self.test_image.shape, (10, 10))
        self.assertTrue(np.all(self.test_image == 255))

    def test_resize_and_show_images(self):
        cv2.imshow = Mock()
        img = prepare_blank_image((10, 10))
        self.assertIsNone(resize_and_show_images(img,
                                                 self.test_control_points))

    def test_get_parts(self):
        parts = []
        get_parts(self.test_control_points, 2, parts)
        self.assertEqual(len(parts), 4)

    # ------------ automated_functions.py ------------

    def test_gabor_filter_automated(self):
        results = gabor_filter_automated(
            get_absolute_path('tests/data/gabor_filter'))
        self.assertEqual(len(results), 2)
        if results[0].shape == (62, 51):
            self.assertTupleEqual(results[0].shape, (62, 51))
            self.assertTupleEqual(results[1].shape, (29, 29))
        else:
            self.assertTupleEqual(results[1].shape, (62, 51))
            self.assertTupleEqual(results[0].shape, (29, 29))

    def test_skeletonize_automated(self):
        results = skeletonize_automated(
            get_absolute_path('tests/data/skeletonization'))
        self.assertEqual(len(results), 2)
        self.assertTupleEqual(results[1].shape, (62, 51))
        self.assertTupleEqual(results[0].shape, (29, 29))

    def test_process_dataset(self):
        cv2.imwrite = Mock()
        try:
            process_dataset(get_absolute_path(
                'tests/data/skeletonization_gabor_filter'))
        except Exception:
            self.fail('process_dataset raised error unexpectedly')

    # ------------ binary_search_filter.py ------------

    def test_binary_search_filter(self):
        result = binary_search_filter(self.test_control_points, 3, 2)
        self.assertIsNotNone(result)
        self.assertTupleEqual(result.shape, (17, 16))

    # ------------ gabor_filter.py ------------

    def test_gabor_filer(self):
        image = get_image(get_absolute_path(
            'tests/data/skeletonization/0.png'))
        result = gabor_filter(image)
        self.assertIsNotNone(result)

    # ------------ skeletonize.py ------------

    def test_skeletonize_image(self):
        image = get_image(get_absolute_path(
            'tests/data/skeletonization/0.png'))
        result = skeletonize_image(image)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
