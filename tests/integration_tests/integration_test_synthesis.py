from src.file_handler.file_handler import get_absolute_path
import cv2
from src.synthesis.control_points import find_control_points, find_cycles, is_neighbour_pixel, left_only_control_points, remove_cycles, skeleton_to_graph
from src.synthesis.get_sequences import get_sequences
import unittest
import random


class SynthesisIntegrationTests(unittest.TestCase):
    """
    The class tests methods from image processing functions.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('\n[START]  Synthesis Integration Tests')

    @classmethod
    def tearDownClass(cls):
        """ after all tests """
        print('\n[END]    Synthesis Integration Tests')

    @classmethod
    def setUp(cls):
        """ before each test """

    def test_find_control_points(self):
        path_to_image = get_absolute_path(
            './tests/data/control_points.png')
        image = cv2.imread(path_to_image)
        self.assertIsNotNone(image)
        result = find_control_points(image)
        self.assertTrue(len(result) == 5)

    def test_skeleton_to_graph(self):
        path_to_image = get_absolute_path(
            './tests/data/test.png')
        image = cv2.imread(path_to_image)
        self.assertIsNotNone(image)
        vertices, edges = skeleton_to_graph(image)
        self.assertTrue(len(vertices) == 32)
        self.assertFalse(len(edges) == 0)

    def test_skeleton_to_graph_and_find_cycles(self):
        path_to_image = get_absolute_path(
            './tests/data/test.png')
        image = cv2.imread(path_to_image)
        self.assertIsNotNone(image)
        vertices, edges = skeleton_to_graph(image)
        result = find_cycles(vertices, edges)
        self.assertTrue(len(result) == 1)

    def test_skeleton_to_graph_find_cycles_remove_cycles(self):
        path_to_image = get_absolute_path(
            './tests/data/test.png')
        image = cv2.imread(path_to_image)
        self.assertIsNotNone(image)
        vertices, edges = skeleton_to_graph(image)
        vertices, edges = remove_cycles(vertices, edges)
        result = find_cycles(vertices, edges)
        self.assertTrue(len(result) == 0)

    def test_get_sequences(self):
        path_to_image = get_absolute_path(
            './tests/data/test.png')
        image = cv2.imread(path_to_image)
        self.assertIsNotNone(image)
        vertices, edges = skeleton_to_graph(image)
        vertices, edges = remove_cycles(vertices, edges)
        result = get_sequences(list(edges))
        for sequence in result:
            for i in range(len(sequence) - 2):
                self.assertTrue(is_neighbour_pixel(
                    sequence[i], sequence[i + 1]))

    def test_left_only_control_points(self):
        path_to_image = get_absolute_path(
            './tests/data/test.png')
        image = cv2.imread(path_to_image)
        self.assertIsNotNone(image)
        vertices, edges = skeleton_to_graph(image)
        vertices, edges = remove_cycles(vertices, edges)
        sequences = get_sequences(list(edges))
        points = random.sample(vertices, 15)
        result = left_only_control_points(sequences, points)
        for sequence in result:
            for element in sequence:
                self.assertTrue(element in points or (
                    element[1], element[0]) in points)

    def test_generate_bsplain_fig(self):
        pass


if __name__ == '__main__':
    unittest.main()
