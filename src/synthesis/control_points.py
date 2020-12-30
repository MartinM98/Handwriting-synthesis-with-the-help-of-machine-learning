from src.synthesis.handwriting_reconstruction import draw_letter
from src.file_handler.file_handler import combine_paths, ensure_create_dir, get_absolute_path, get_dir_path
from src.synthesis.get_sequences import get_sequences
from src.synthesis.get_sequences2 import get_sequences2
import cv2
from matplotlib import pyplot as plt
import numpy as np
import math
import multiprocessing
from glob import glob
from src.synthesis.generate_letter import generate_letter
from src.file_handler.file_handler import get_file_name
from src.image_processing.resize import resize_image


def is_neighbour_pixel(p1: tuple, p2: tuple):
    """
    Check if pixels are neighbours.

    Args:
        p1 (tuple): First pixel.
        p2 (tuple): Second pixel.

    Returns:
        (bool): True if pixels are neighbours, False otherwise.
    """
    if abs(p1[0] - p2[0]) < 2 and abs(p1[1] - p2[1]) < 2:
        return True
    return False


def points_distance(p1: tuple, p2: tuple):
    """
    Retrun distannce between points.

    Args:
        p1 (tuple): First point.
        p2 (tuple): Second point.

    Returns:
        (int)): Distance between points
    """
    return math.sqrt(
        ((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2))


def find_neighbours(vertex: list, edges: set):
    """
    Find in edges all connected vertices with the vertex.

    Args:
        vertices (list): List of vertices.
        edges (set): Set of edges as pairs of connected points.

    Returns:
        result (set): All connected vertices with the vertex.
    """
    result = set()
    for e in edges:
        if e[0] == vertex:
            result.add(e[1])
        elif e[1] == vertex:
            result.add(e[0])
    return result


def remove_edge(edges: set, v1: tuple, v2: tuple):
    """
    Remove from set edges the edge between vertices v1 and v2.

    Args:
        edges (set): Set of edges as pairs of connected points.
        v1 (tuple): First point.
        v2 (tuple): Second point.
    """
    edges.discard((v1, v2))
    edges.discard((v2, v1))


def find_control_points(image_with_control_points):
    """
    Search control points from the input image and return the list of the points.

    Args:
        image_with_control_points (image): Image with control points.

    Returns:
        list: List of control points
    """
    if len(image_with_control_points.shape) == 3:
        gray = cv2.cvtColor(image_with_control_points, cv2.COLOR_BGR2GRAY)
    else:
        gray = image_with_control_points
    threshold_level = 50
    vertices = np.column_stack(np.where(gray < threshold_level))
    return [(v[0], v[1]) for v in vertices]


def skeleton_to_graph(image):
    """
    Produce graph from image of skeleton.

    Args:
        image: image of skeleton.

    Returns:
        vertices(list): List of vertices.
        edges(set): Set of edges as pairs of connected points.
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    threshold_level = 50
    vertices = np.column_stack(np.where(gray < threshold_level))
    vertices = [(v[0], v[1]) for v in vertices]

    edges = set()
    for v in vertices:
        for ver in vertices:
            if ver is not v and is_neighbour_pixel(v, ver) and not (ver, v) in edges:
                edges.add((v, ver))

    return vertices, edges


def draw_graph(vertices: list, edges: set):
    """
    Drawing a graph

    Args:
        vertices(list): List of vertices.
        edges(set): Set of edges as pairs of connected points.
    """
    x_number_list = [v[0] for v in vertices]
    y_number_list = [v[1] for v in vertices]

    plt.axis([min(x_number_list) - 1, max(x_number_list) + 1,
              min(y_number_list) - 1, max(y_number_list) + 1])
    plt.scatter(x_number_list, y_number_list, s=10)

    for e in edges:
        x = list()
        y = list()
        x.append(e[0][0])
        x.append(e[1][0])
        y.append(e[0][1])
        y.append(e[1][1])
        plt.plot(x, y)

    plt.show()


def find_cycles(vertices: list, edges: set):
    """
    Find all cycles in the graph (vertices, edges) and result the edges which create a cycle.

    Args:
        vertices(list): List of vertices.
        edges(set): Set of edges as pairs of connected points.

    Returns:
        result (set(frozenset)): Set includes cycles (set of edges).
    """
    result = set()
    for vertex in vertices:
        neighbours = find_neighbours(vertex, edges)
        if len(neighbours) > 1:
            all_neighbours = set()
            for neighbour in neighbours:
                neighbour_neighbours = find_neighbours(neighbour, edges)
                common = neighbours.intersection(neighbour_neighbours)
                all_neighbours = all_neighbours.union(common)
            if len(all_neighbours) >= 2:
                all_neighbours.add(vertex)
                result.add(frozenset(all_neighbours))
    to_remove = set()
    for res in result:
        for r in result:
            if res is not r and res.issubset(r):
                to_remove.add(res)
    result = result - to_remove
    return result


def remove_cycles(vertices: list, edges: set):
    """
    Remove all cycles from graph(vertices, edges) and return graph(vertices, edges) without cycles.

    Args:
        vertices(list): List of vertices.
        edges(set): Set of edges as pairs of connected points.

    Returns:
        vertices(list): List of vertices.
        edges(set): Set of edges as pairs of connected points.
    """
    cycles = find_cycles(vertices, edges)
    for cycle in cycles:
        for c1 in cycle:
            for c2 in cycle:
                if c1 is not c2 and points_distance(c1, c2) > 1:
                    remove_edge(edges, c1, c2)

    return vertices, edges


def left_only_control_points(letter: list, control_points: list):
    """
    Remove all points from letter if the point is not in the list control_points.

    Args:
        letter (list): Letter in form of list
        control_points (list): List of control points.

    Returns:
        list: New letter in form of list.
    """
    new_letter = list()
    for line in letter:
        new_line = list()
        for point in line:
            if point in control_points or (point[1], point[0]) in control_points:
                new_line.append(point)
        new_letter.append(new_line)
    return new_letter


def produce_imitation(path_to_skeleton: str, path_to_control_points: str, path_to_control_points2: str, idx: int, font_size: int = None):
    """
    Produce imitation of the letter form the skeleton.

    Args:
        path_to_skel (str): Path to skeleton of letter.
    """
    image = cv2.imread(path_to_skeleton)
    image = cv2.rotate(image, cv2.cv2.ROTATE_90_CLOCKWISE)
    image_control_points = cv2.imread(path_to_control_points)
    image_control_points = cv2.rotate(
        image_control_points, cv2.cv2.ROTATE_90_CLOCKWISE)
    image_control_points2 = cv2.imread(path_to_control_points2)
    image_control_points2 = cv2.rotate(
        image_control_points2, cv2.cv2.ROTATE_90_CLOCKWISE)
    control_points = find_control_points(image_control_points)
    height, width, _ = image.shape
    if font_size is not None:
        height = int(height * font_size)
        width = int(width * font_size)
    vertices, edges = skeleton_to_graph(image)
    remove_cycles(vertices, edges)
    result = list()
    result = get_sequences(list(edges))
    # result = list(r for r in result if len(r) > 2)
    letter = left_only_control_points(result, control_points)
    new_letter = generate_letter(
        path_to_control_points, path_to_control_points2)
    letter2 = match_points(letter, new_letter)
    letter3 = []
    for line in letter2:
        letter3.append(list(dict.fromkeys(line)))
    file_name = get_file_name(path_to_skeleton).replace(
        '_skel', '_bspline' + str(idx))
    path_to_save = get_dir_path(get_dir_path(path_to_skeleton))
    path_to_save = combine_paths(path_to_save, 'bspline')
    path_to_save = combine_paths(path_to_save, file_name)
    width = max(image_control_points.shape[0], image_control_points2.shape[0])
    height = max(image_control_points.shape[1], image_control_points2.shape[1])
    draw_letter(letter3, path_to_save_file=path_to_save,
                image_size=(width, height), skeleton_flag=True)


def produce_bspline(image: np.ndarray, image_control_points: np.ndarray, image_control_points2: np.ndarray, idx: int, match_with_other: bool, font_size: int = None):
    """
    Produce imitation of the letter form the skeleton.

    Args:
        path_to_skel (str): Path to skeleton of letter.

    Returns:
        np.ndarray: a generated bspline.
    """
    control_points = find_control_points(image_control_points)
    height, width, _ = image.shape
    if font_size is not None:
        height = int(height * font_size)
        width = int(width * font_size)
    vertices, edges = skeleton_to_graph(image)
    remove_cycles(vertices, edges)
    result = list()
    result = get_sequences(list(edges))
    # result = list(r for r in result if len(r) > 2)
    letter = left_only_control_points(result, control_points)
    width = image_control_points.shape[0]
    height = image_control_points.shape[1]
    if match_with_other:
        new_letter = generate_letter(image_control_points, image_control_points2)
        letter2 = match_points(letter, new_letter)
        letter3 = []
        for line in letter2:
            letter3.append(list(dict.fromkeys(line)))
        width = max(image_control_points.shape[0], image_control_points2.shape[0])
        height = max(image_control_points.shape[1], image_control_points2.shape[1])
        letter = letter3
    path_to_save = combine_paths('./data/synthesis/skeletons/', str(idx) + '.png')
    bspline_image = draw_letter(letter, image_size=(width, height), skeleton_flag=True, show_flag=False)
    bspline_image = resize_image('', 256, 256, image=bspline_image)
    cv2.imwrite(path_to_save, bspline_image)


def produce_imitation_set(path_to_letters: str):
    """
    Generate imitation for all skeletons in the path.

    Args:
        path_to_letters (str): Path to directory containing skeletons.
    """
    paths_to_skeletons = [f for f in glob(
        combine_paths(path_to_letters, '**', '*_skel.png'), recursive=True)]

    for path_to_skeleton in paths_to_skeletons:
        path_to_save = get_dir_path(get_dir_path(path_to_skeleton))
        path_to_save = combine_paths(path_to_save, 'bspline')
        ensure_create_dir(path_to_save)

    iterable = [(path) for path in paths_to_skeletons]

    p = multiprocessing.Pool()
    p.map_async(produce_imitation, iterable)

    p.close()
    p.join()  # Wait for all child processes to close.


def match_points(letter: list, new_letter: list):
    """
    Matches the generated points to the base letter.

    Args:
        letter (list): The list of the base letter.
        new_letter (list): The list of tuples of base image's points
        and generated points.

    Returns:
        (list): List of generated points matched to the points
        of the base letter.
    """
    new = list()
    for line in letter:
        new_line = list()
        for point in line:
            for i in new_letter:
                if (i[0][0] == point[0]) and (i[0][1] == point[1]):
                    new_line.append(i[1])
        new.append(new_line)
    return new


def test():
    """
    Testing
    """
    path_to_skeleton = get_absolute_path(
        './src/graphical_interface/letters_dataset/A/skel/1_skel.png')
    path_to_control_points = get_absolute_path(
        './src/graphical_interface/letters_dataset/A/skel/1_skel_control_points.png')
    path_to_control_points2 = get_absolute_path(
        './src/graphical_interface/letters_dataset/A/skel/2_skel_control_points.png')
    image_skeleton = cv2.imread(path_to_skeleton)
    image_skeleton = cv2.rotate(image_skeleton, cv2.cv2.ROTATE_90_CLOCKWISE)
    image_control_points = cv2.imread(path_to_control_points)
    image_control_points = cv2.rotate(
        image_control_points, cv2.cv2.ROTATE_90_CLOCKWISE)
    image_control_points2 = cv2.imread(path_to_control_points2)
    image_control_points2 = cv2.rotate(
        image_control_points2, cv2.cv2.ROTATE_90_CLOCKWISE)
    vertices, edges = skeleton_to_graph(image_skeleton)
    control_points = find_control_points(image_control_points)
    # draw_graph(vertices, edges)
    remove_cycles(vertices, edges)
    # draw_graph(vertices, edges)
    result = get_sequences2(list(edges))
    # res = [r for r in result if len(r) > 2]
    print("control points", control_points, '\n')
    print("res", result, '\n')
    letter = left_only_control_points(result, control_points)
    print("letter", result, '\n')
    new_letter = generate_letter(
        path_to_control_points, path_to_control_points2)
    letter2 = match_points(letter, new_letter)
    letter3 = []
    for line in letter2:
        letter3.append(list(dict.fromkeys(line)))
    print('generated', letter3)
    width = max(image_control_points.shape[0], image_control_points2.shape[0])
    height = max(image_control_points.shape[1], image_control_points2.shape[1])
    draw_letter(letter3, path_to_save_file='./test.png',
                image_size=(width, height), skeleton_flag=True)


if __name__ == '__main__':
    test()
    # path_to_letters = get_absolute_path(
    #     './src/graphical_interface/letters_dataset/')
    # produce_imitation_set(path_to_letters)
