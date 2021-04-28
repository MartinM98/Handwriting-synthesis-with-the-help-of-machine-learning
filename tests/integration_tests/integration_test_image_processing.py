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

# ------------ binary_search_filter.py ------------
from src.image_processing.binary_search_filter import binary_search_filter

# ------------ gabor_filter.py ------------
from src.image_processing.gabor_filter import gabor_filter

# ------------ skeletonize.py ------------
from src.image_processing.skeletonize import skeletonize_image

# ------------ automated_functions.py.py ------------
from src.image_processing.automated_functions import filter_image
from src.image_processing.automated_functions import prepare_images
from src.image_processing.automated_functions import process_dataset


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
    @unittest.skip("work in progress")
    def test_get_dir_and_file(self):
        filedialog.askopenfilename = Mock(return_value='/usr/local/test.png')
        Tk = Mock(return_value=None)
        print('test12')
        Tk.withdraw = Mock()
        Tk.destroy = Mock()
        self.assertTupleEqual(get_dir_and_file(),
                              ('/usr/local', 'test', '/usr/local/test.png'))
        filedialog.askopenfilename = Mock(return_value='')
        self.assertTupleEqual(get_dir_and_file(), ('', '', ''))

    @unittest.skip("work in progress")
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
        image = cv2.imread(get_absolute_path(
            'tests/data/skeletonization/0.png'))
        result = skeletonize_image(image)
        self.assertIsNotNone(result)

    # ------------ automated_functions.py.py ------------

    def test_filter_image(self):
        image = self.test_control_points.copy()
        width, height = image.shape
        size = width * height
        self.assertTrue((filter_image(image, 'Original', 0, 0) == image).all())
        image = self.test_control_points.copy()
        self.assertEqual(len(np.nonzero(filter_image(image, 'Consecutive', 2, 3))[0]), size - 3)
        image = self.test_control_points.copy()
        self.assertEqual(len(np.nonzero(filter_image(image, 'Random', 2, 3))[0]), size - 3)
        image = self.test_control_points.copy()
        self.assertEqual(len(np.nonzero(filter_image(image, 'BS', 2, 3))[0]), size - 3)

    def test_prepare_images(self):
        skeleton_path = 'tests/data/gabor_filter/0_skel.png'
        control_points_path = 'tests/data/filtering/0_skel_control_points.png'
        skeleton_test = cv2.imread('tests/data/gabor_filter/0_skel_rotated.png')
        control_points_test = cv2.imread(control_points_path)
        control_points_test = cv2.rotate(control_points_test, cv2.cv2.ROTATE_90_CLOCKWISE)
        result = prepare_images(skeleton_path, control_points_path, control_points_path, 0, 0, 'Original')
        self.assertTrue((result[0] == skeleton_test).all())
        self.assertTrue((result[1] == control_points_test).all())

        control_points_test = cv2.cvtColor(control_points_test, cv2.COLOR_BGR2GRAY)
        width, height = control_points_test.shape
        size = width * height
        skeleton_test = cv2.imread('tests/data/gabor_filter/0_skel_rotated.png')
        result = prepare_images(skeleton_path, control_points_path, control_points_path, 10, 10, 'BS')
        self.assertTrue((result[0] == skeleton_test).all())
        self.assertEqual(len(np.nonzero(result[1])[0]), size - 10)

        result = prepare_images(skeleton_path, control_points_path, control_points_path, 10, 7, 'Consecutive')
        self.assertTrue((result[0] == skeleton_test).all())
        self.assertEqual(len(np.nonzero(result[1])[0]), size - 7)

        result = prepare_images(skeleton_path, control_points_path, control_points_path, 10, 1, 'Random')
        self.assertTrue((result[0] == skeleton_test).all())
        self.assertEqual(len(np.nonzero(result[1])[0]), size - 1)

    def test_process_dataset(self):
        try:
            process_dataset('tests/data/process_dataset_test')
        except Exception:
            self.fail('process_dataset raised error unexpectedly')


if __name__ == '__main__':
    unittest.main()
