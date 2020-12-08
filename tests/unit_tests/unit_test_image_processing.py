import unittest
from src.image_processing.letters import check_char
import numpy as np
from src.file_handler.file_handler import get_absolute_path

# ------------ common_functions.py ------------
from src.image_processing.common_functions.common_functions import process_part
from src.image_processing.common_functions.common_functions import get_image
from src.image_processing.common_functions.common_functions import get_dimensions
from src.image_processing.common_functions.common_functions import get_box
from src.image_processing.common_functions.common_functions import prepare_blank_image
from src.image_processing.common_functions.common_functions import get_parts

# ------------ binary_search_filter.py ------------
from src.image_processing.binary_search_filter import add_end_points
from src.image_processing.binary_search_filter import add_point

# ------------ gabor_filter.py ------------
from src.image_processing.gabor_filter import check_point
from src.image_processing.gabor_filter import shift_point
from src.image_processing.gabor_filter import fit_points


class ImageProcessingUnitTests(unittest.TestCase):
    """
    The class tests methods from image processing functions.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('\n[START]  Image Processing Unit Tests')
        cls.test_image = prepare_blank_image(shape=(10, 10))
        cls.test_control_points = get_image(
            get_absolute_path('tests/data/control_points.png'))
        cls.parts = []
        get_parts(cls.test_control_points, 3, cls.parts)

    @classmethod
    def tearDownClass(cls):
        """ after all tests """
        print('\n[END]    Image Processing Unit Tests')

    @classmethod
    def setUp(cls):
        """ before each test """

    def test_name(self):
        pass

    def test_check_char(self):
        path = './tests/data'
        lower = check_char(path, 'a')
        upper = check_char(path, 'A')
        colon = check_char(path, ':')
        dot = check_char(path, '.')
        question = check_char(path, '?')
        asterisk = check_char(path, '*')
        self.assertTrue(lower == './tests/data/a2/')
        self.assertTrue(upper == './tests/data/A/')
        self.assertTrue(colon == './tests/data/colon/')
        self.assertTrue(dot == './tests/data/dot/')
        self.assertTrue(question == './tests/data/question/')
        self.assertTrue(asterisk == './tests/data/asterisk/')

    # ------------ common_functions.py ------------

    def test_process_part(self):
        points = process_part(self.test_control_points, 0, 0, 6, 6)
        self.assertEqual(len(points), 1)
        points = process_part(self.test_control_points, 6, 6,
                              self.test_control_points.shape[0] - 1, self.test_control_points.shape[1] - 1)
        self.assertEqual(len(points), 2)
        points = process_part(self.test_control_points, 0, 0, 6, 6)
        self.assertEqual(len(points), 1)

    def test_get_dimensions(self):
        self.assertTupleEqual(get_dimensions(
            self.test_control_points, 2), (17, 16, 9, 8))
        self.assertTupleEqual(get_dimensions(
            self.test_control_points, 3), (17, 16, 6, 6))

    def test_get_box(self):
        self.assertTupleEqual(get_box(0, 5, 10, 0, 5, 10,), (0, 4, 0, 4))
        self.assertTupleEqual(get_box(8, 5, 10, 0, 5, 10,), (8, 9, 0, 4))
        self.assertTupleEqual(get_box(6, 5, 10, 6, 5, 10,), (6, 9, 6, 9))

    # ------------ binary_search_filter.py ------------

    def test_add_end_points(self):
        halves = []
        parts2 = [part for part in self.parts if len(part) > 0]
        img = prepare_blank_image(shape=(20, 20))
        add_end_points(halves, img, parts2)
        self.assertEqual(len(halves), 2)
        count = 0
        for ix, iy in np.ndindex(img.shape):
            if img[ix, iy] == 0:
                count += 1
        self.assertEqual(count, 2)

    def test_add_point(self):
        halves = [0, 2]
        tmp = [0, 2]
        img = prepare_blank_image(shape=(20, 20))
        parts2 = [part for part in self.parts if len(part) > 0]
        add_point(img, tmp, halves, 0, parts2, 0)
        self.assertEqual(len(tmp) - len(halves), 1)
        count = 0
        for ix, iy in np.ndindex(img.shape):
            if img[ix, iy] == 0:
                count += 1
        self.assertEqual(count, 1)

    # ------------ gabor_filter.py ------------

    def test_check_point(self):
        self.assertTrue(check_point(
            self.test_control_points, [5, 3], 1, 16))
        self.assertTrue(check_point(
            self.test_control_points, [0, 0], 1, 16))
        self.assertFalse(check_point(
            self.test_control_points, [16, 0], 1, 16))
        self.assertTrue(check_point(
            self.test_control_points, [14, 0], 2, 15))
        self.assertFalse(check_point(
            self.test_control_points, [7, 6], 1, 16))

    def test_shift_points(self):
        img = self.test_control_points.copy()
        shift_point(img, [4, 3], -1, 16)
        self.assertTrue(img[3, 3] == 0)
        self.assertTrue(img[4, 3] == 255)
        img[15, 3] = 0
        shift_point(img, [15, 3], -1, 15)
        self.assertTrue(img[15, 3] == 0)

    def test_fit_points(self):
        img = self.test_control_points.copy()
        img2 = self.test_control_points.copy()
        for ix, iy in np.ndindex(img.shape):
            if img[ix, iy] == 0:
                img[ix, iy] = 255
                img[ix - 1, iy] = 0
        fit_points(img, img2)
        for ix, iy in np.ndindex(img.shape):
            self.assertEqual(img[ix, iy], img2[ix, iy])


if __name__ == '__main__':
    unittest.main()
