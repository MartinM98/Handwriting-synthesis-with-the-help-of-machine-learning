from src.synthesis.handwriting_reconstruction import generate_bsplain
from src.synthesis.control_points import find_neighbours, is_neighbour_pixel, points_distance, remove_edge
import unittest

# ------------ get_sequences2.py ------------
from src.synthesis.get_sequences2 import compare_points
from src.synthesis.get_sequences2 import get_points
from src.synthesis.get_sequences2 import find_non_zero_occurence_point
from src.synthesis.get_sequences2 import find_single_occurence_point


class SynthesisUnitTests(unittest.TestCase):
    """
    The class tests methods from image processing functions.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('\n[START]  Synthesis Unit Tests')
        cls.p1 = (0, 0)
        cls.p2 = (0, 1)
        cls.p3 = (3, 0)
        cls.edges = set()
        cls.edges.add((cls.p1, cls.p2))
        cls.edges.add((cls.p2, cls.p3))
        cls.edges2 = (((39, 3), (40, 3)), ((19, 12), (20, 12)), ((17, 14), (18, 13)), ((16, 14), (17, 14)), ((9, 19), (10, 19)), ((22, 11), (23, 10)), ((33, 5), (34, 4)), ((38, 3), (39, 3)), ((21, 11), (22, 11)), ((44, 2), (45, 2)), ((49, 6), (49, 7)), ((26, 8), (27, 8)), ((49, 7), (49, 8)), ((37, 3), (38, 3)), ((47, 3), (48, 4)), ((48, 15), (48, 16)), ((34, 4), (35, 4)), ((46, 19), (46, 20)), ((35, 4), (36, 4)), ((18, 13), (19, 12)), ((25, 9), (26, 8)), ((4, 24), (5, 23)), ((48, 4), (49, 5)), ((36, 4), (37, 3)), ((41, 3), (42, 2)), ((49, 9), (49, 10)), ((14, 16), (15, 15)), ((13, 17), (14, 16)), ((45, 2), (46, 3)), ((48, 12), (48, 13)), ((12, 17), (13, 17)), ((31, 6), (32, 5)), ((47, 17), (47, 18)), ((15, 15), (16, 14)), ((48, 12), (49, 11)), ((
            43, 2), (44, 2)), ((43, 25), (43, 26)), ((48, 13), (48, 14)), ((7, 21), (8, 20)), ((27, 8), (28, 8)), ((24, 9), (25, 9)), ((28, 8), (29, 7)), ((23, 10), (24, 9)), ((46, 19), (47, 18)), ((8, 20), (9, 19)), ((6, 22), (7, 21)), ((29, 7), (30, 6)), ((47, 17), (48, 16)), ((5, 23), (6, 22)), ((11, 18), (12, 17)), ((30, 6), (31, 6)), ((41, 28), (42, 27)), ((42, 27), (43, 26)), ((44, 23), (44, 24)), ((40, 3), (41, 3)), ((1, 26), (2, 25)), ((10, 19), (11, 18)), ((32, 5), (33, 5)), ((42, 2), (43, 2)), ((45, 21), (45, 22)), ((49, 5), (49, 6)), ((49, 8), (49, 9)), ((49, 10), (49, 11)), ((48, 14), (48, 15)), ((2, 25), (3, 24)), ((45, 21), (46, 20)), ((46, 3), (47, 3)), ((44, 23), (45, 22)), ((3, 24), (4, 24)), ((43, 25), (44, 24)), ((20, 12), (21, 11)))

    @classmethod
    def tearDownClass(cls):
        """ after all tests """
        print('\n[END]    Synthesis Unit Tests')

    @classmethod
    def setUp(cls):
        """ before each test """
        cls.edges.clear()
        cls.edges.add((cls.p1, cls.p2))
        cls.edges.add((cls.p2, cls.p3))

    def test_is_neighbour_pixel(self):
        self.assertTrue(is_neighbour_pixel(self.p1, self.p2))
        self.assertFalse(is_neighbour_pixel(self.p1, self.p3))

    def test_points_distance(self):
        self.assertEqual(points_distance(self.p1, self.p2), 1)
        self.assertEqual(points_distance(self.p1, self.p3), 3)

    def test_find_neighbours(self):
        result1 = find_neighbours(self.p1, self.edges)
        self.assertEqual(len(result1), 1)
        self.assertIn(self.p2, result1)
        result1 = find_neighbours(self.p2, self.edges)
        self.assertEqual(len(result1), 2)
        self.assertIn(self.p1, result1)
        self.assertIn(self.p3, result1)

    def test_remove_edge(self):
        self.assertTrue(len(self.edges) == 2)
        remove_edge(self.edges, self.p1, self.p2)
        self.assertTrue(len(self.edges) == 1)
        remove_edge(self.edges, self.p1, self.p2)
        self.assertTrue(len(self.edges) == 1)

    def test_generate_bsplain(self):
        x = [1, 2, 3]
        y = [3, 4, 5]
        result = generate_bsplain(x, y)
        self.assertIsNotNone(result)
        self.assertTrue(len(result) == 2)

    # ------------ get_sequences2.py ------------

    def test_compare_points(self):
        self.assertTrue(compare_points([14, 1], [14, 1]))
        self.assertFalse(compare_points([1, 14], [14, 1]))

    def test_find_non_zero_occurence_point(self):
        points = get_points(self.edges2)
        index = 14
        for i in points:
            i[1] = 0
        points[index][1] = 1

        self.assertEqual(find_non_zero_occurence_point(points), index)

    def test_find_single_occurence_point(self):
        points = get_points(self.edges2)
        index = 14
        for i in points:
            i[1] = 10
        points[index][1] = 1

        self.assertEqual(find_single_occurence_point(points), index)


if __name__ == '__main__':
    unittest.main()
