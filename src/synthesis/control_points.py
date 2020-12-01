from src.synthesis.handwriting_reconstruction import draw_letter
from src.file_handler.file_handler import combine_paths, ensure_create_dir, get_absolute_path, get_dir_path, get_file_name
from src.synthesis.get_sequences import get_sequences
import cv2
from matplotlib import pyplot as plt
import numpy as np
import math
import multiprocessing
from glob import glob


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


def skeleton_to_graph(image):
    """
    Produce graph from image of skeleton.

    Args:
        image: image of skeleton.

    Returns:
        vertices(list): List of vertices.
        edges(set): Set of edges as pairs of connected points.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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


def produce_imitation(path_to_skeleton: str):
    """
    Produce imitation of the letter form the skeleton.

    Args:
        path_to_skel (str): Path to skeleton of letter.
    """
    image = cv2.imread(path_to_skeleton)
    height, width, _ = image.shape
    vertices, edges = skeleton_to_graph(image)
    remove_cycles(vertices, edges)
    result = list()
    result = get_sequences(list(edges))
    result = list(r for r in result if len(r) > 2)
    file_name = get_file_name(path_to_skeleton).replace('_skel', '_bspline')
    path_to_save = get_dir_path(get_dir_path(path_to_skeleton))
    path_to_save = combine_paths(path_to_save, 'bspline')
    path_to_save = combine_paths(path_to_save, file_name)
    draw_letter(result, path_to_save_file=path_to_save,
                image_size=(height, width))


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


def test():
    """
    Testing
    """
    path_to_skeleton = get_absolute_path(
        './src/graphical_interface/letters_dataset/A/skel/0_skel.png')
    vertices, edges = skeleton_to_graph(path_to_skeleton)
    draw_graph(vertices, edges)
    remove_cycles(vertices, edges)
    draw_graph(vertices, edges)
    result = get_sequences(list(edges))
    res = [r for r in result if len(r) > 2]
    draw_letter(res)


if __name__ == '__main__':
    # test()
    path_to_letters = get_absolute_path(
        './src/graphical_interface/letters_dataset/')
    produce_imitation_set(path_to_letters)
