from src.file_handler.file_handler import get_absolute_path
import cv2
from src.synthesis.control_points import find_control_points, find_cycles, is_neighbour_pixel, left_only_control_points, remove_cycles, skeleton_to_graph
from src.synthesis.get_sequences import get_sequences
import unittest
import random
import numpy as np

# ------------ get_sequences2.py ------------
from src.synthesis.get_sequences_extended import get_unique_points
from src.synthesis.get_sequences_extended import get_points
from src.synthesis.get_sequences_extended import get_point_index
from src.synthesis.get_sequences_extended import decrement_point_occur
from src.synthesis.get_sequences_extended import init_append
from src.synthesis.get_sequences_extended import one_way_append
from src.synthesis.get_sequences_extended import get_sequences_extended


class SynthesisIntegrationTests(unittest.TestCase):
    """
    The class tests methods from image processing functions.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('\n[START]  Synthesis Integration Tests')
        cls.edges2 = (((39, 3), (40, 3)), ((19, 12), (20, 12)), ((17, 14), (18, 13)), ((16, 14), (17, 14)), ((9, 19), (10, 19)), ((22, 11), (23, 10)), ((33, 5), (34, 4)), ((38, 3), (39, 3)), ((21, 11), (22, 11)), ((44, 2), (45, 2)), ((49, 6), (49, 7)), ((26, 8), (27, 8)), ((49, 7), (49, 8)), ((37, 3), (38, 3)), ((47, 3), (48, 4)), ((48, 15), (48, 16)), ((34, 4), (35, 4)), ((46, 19), (46, 20)), ((35, 4), (36, 4)), ((18, 13), (19, 12)), ((25, 9), (26, 8)), ((4, 24), (5, 23)), ((48, 4), (49, 5)), ((36, 4), (37, 3)), ((41, 3), (42, 2)), ((49, 9), (49, 10)), ((14, 16), (15, 15)), ((13, 17), (14, 16)), ((45, 2), (46, 3)), ((48, 12), (48, 13)), ((12, 17), (13, 17)), ((31, 6), (32, 5)), ((47, 17), (47, 18)), ((15, 15), (16, 14)), ((48, 12), (49, 11)), ((
            43, 2), (44, 2)), ((43, 25), (43, 26)), ((48, 13), (48, 14)), ((7, 21), (8, 20)), ((27, 8), (28, 8)), ((24, 9), (25, 9)), ((28, 8), (29, 7)), ((23, 10), (24, 9)), ((46, 19), (47, 18)), ((8, 20), (9, 19)), ((6, 22), (7, 21)), ((29, 7), (30, 6)), ((47, 17), (48, 16)), ((5, 23), (6, 22)), ((11, 18), (12, 17)), ((30, 6), (31, 6)), ((41, 28), (42, 27)), ((42, 27), (43, 26)), ((44, 23), (44, 24)), ((40, 3), (41, 3)), ((1, 26), (2, 25)), ((10, 19), (11, 18)), ((32, 5), (33, 5)), ((42, 2), (43, 2)), ((45, 21), (45, 22)), ((49, 5), (49, 6)), ((49, 8), (49, 9)), ((49, 10), (49, 11)), ((48, 14), (48, 15)), ((2, 25), (3, 24)), ((45, 21), (46, 20)), ((46, 3), (47, 3)), ((44, 23), (45, 22)), ((3, 24), (4, 24)), ((43, 25), (44, 24)), ((20, 12), (21, 11)))

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

    # ------------ get_sequences2.py ------------

    def test_get_unique_points(self):
        result = get_unique_points(self.edges2)
        self.assertEqual(len(result), len(self.edges2) + 1)

    def test_get_points(self):
        result = get_points(self.edges2)
        self.assertEqual(len(result), len(self.edges2) + 1)
        sum = 0
        for i in result:
            sum += i[1]
        self.assertEqual(sum, len(self.edges2) * 2)
        leaves = 0
        for i in result:
            if i[2] == 1:
                leaves += 1
        self.assertEqual(len(result) + 1 - leaves,
                         len(self.edges2))

    def test_get_point_index(self):
        points = get_points(self.edges2)
        index = 5
        self.assertEqual(get_point_index(points, points[index][0]), index)
        index = 0
        self.assertEqual(get_point_index(points, points[index][0]), index)
        index = 15
        self.assertEqual(get_point_index(points, points[index][0]), index)
        index = 23
        self.assertEqual(get_point_index(points, points[index][0]), index)

    def test_decrement_point_occur(self):
        points = get_points(self.edges2)
        index = 5
        value = points[index][1]
        decrement_point_occur(points, points[index][0])
        self.assertEqual(points[index][1], value - 1)

    def test_init_append(self):
        points = get_points(self.edges2)
        checked = np.zeros(len(points))
        seq, edg, last = init_append(self.edges2, points, 0, checked)
        self.assertEqual(len(seq), 2)

    def test_one_way_append(self):
        points = get_points(self.edges2)
        checked = np.zeros(len(points))
        index = -1
        for i in range(len(points)):
            if points[i][1] == 1:
                index = i
                break
        result = one_way_append(self.edges2, points, index, checked)
        self.assertEqual(len(result), len(points))

    def test_get_sequences_extended(self):
        result = get_sequences_extended(self.edges2)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), len(self.edges2) + 1)


if __name__ == '__main__':
    unittest.main()
