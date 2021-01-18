import numpy as np


def compare_points(p1: tuple, p2: tuple):
    """
    Comapres two points

    Args:
        p1 (tuple): The first point.
        p2 (tuple): The second point.

    Returns:
        bool: The outcome of the comparision.
    """
    if p1[0] == p2[0] and p1[1] == p2[1]:
        return True
    return False


def get_unique_points(edges: list):
    """
    Creates a list of all unique points that are a part
    of at least one edge.

    Args:
        edges (list): The list of all edges.

    Returns:
        list: list of all unique points.
    """
    points_unique = []
    for edge in edges:
        add1 = True
        add2 = True
        for p in points_unique:
            if compare_points(edge[0], p):
                add1 = False
            elif compare_points(edge[1], p):
                add2 = False
        if add1:
            points_unique.append(edge[0])
        if add2:
            points_unique.append(edge[1])
    return points_unique


def get_points(edges: list):
    """
    Creates a list of all unique points, their number of occurences
    for all points that are a part of at least one edge, and the flag which
    gets information if the point is a vertex connecting different paths.

    Args:
        edges (list): The list of all edges.

    Returns:
        list: list of all unique points and their number of occurences.
    """
    points_unique = get_unique_points(edges)
    points = []
    for p in points_unique:
        elem = []
        elem.append(p)
        elem.append(0)
        elem.append(0)
        points.append(elem)
    for i in range(len(points)):
        for j in range(len(edges)):
            first = compare_points(edges[j][0], points[i][0])
            second = compare_points(edges[j][1], points[i][0])
            if first or second:
                points[i][1] += 1
    exists = False
    for i in range(len(points)):
        if points[i][1] > 2 or points[i][1] == 1:
            points[i][2] = 1
            exists = True
    if not exists:
        points[0][2] = 1

    return points


def get_point_index(points: list, point: tuple):
    """
    Gets an index of a point in the list of all unique points

    Args:
        points (list): The list of all unique points and their number of
        occurences.
        point (tuple): Point which index should be found.

    Returns:
        int: The index of the point in the points list.
    """
    for i in range(len(points)):
        if compare_points(points[i][0], point):
            return i


def decrement_point_occur(points: list, point: tuple):
    """
    Decrements the number of occurences of the given point
    in the points list.

    Args:
        points (list): The list of all unique points and their number of
        occurences.
        point (tuple): Point which index should be found.
    """
    for elem in points:
        if compare_points(elem[0], point):
            elem[1] -= 1


def init_append(edges: list, points: list, index: int, checked: list):
    """
    Appends the vertices from the first edge to the seqeunce.

    Args:
        edges (list): The list of all edges.
        points (list): The list of all unique points, their number of
            occurences and flags indicating if the vertex connects many paths.
        index (int): the index of the first edge in the edges list.

    Returns:
        list: the sequence in one direction with the first two appended points.
        int: the index of the last processed edge.
        tuple: the last processed point.
    """
    sequence = []
    x = -1
    y = -1
    last_index = -1
    for i in range(len(edges)):
        if checked[i] == 0:
            if compare_points(edges[i][1], points[index][0]):
                last_index = i
                x = 0
                y = 1
            if compare_points(edges[i][0], points[index][0]):
                last_index = i
                x = 1
                y = 0
    points[index][1] -= 1
    sequence.append(edges[last_index][y])
    last = edges[last_index][x]
    sequence.append(last)
    idx = get_point_index(points, last)
    points[idx][1] -= 1
    checked[last_index] = 1
    return sequence, last_index, last


def one_way_append(edges: list, points: list, index: int, checked: list):
    """
    Traverses the edges list creating a sequence of points
    in one direction starting with the index'th point in the
    points list.

    Args:
        edges (list): The list of all edges.
        points (list): The list of all unique points and their number of
        occurences.

    Returns:
        list: the sequence in one direction starting with
        the index'th point in the points list.
    """
    sequence, last_index, last = init_append(edges, points, index, checked)
    for i in range(len(edges)):
        for index in range(len(edges)):
            if index != last_index:
                first = compare_points(edges[index][0], last)
                second = compare_points(edges[index][1], last)
                if (first or second) and checked[index] == 0:
                    if first:
                        x = 1
                    if second:
                        x = 0
                    idx = get_point_index(points, last)
                    points[idx][1] -= 1
                    idx = get_point_index(points, edges[index][x])
                    checked[index] = 1
                    if points[idx][1] == 2 and points[idx][2] == 0:
                        sequence.append(edges[index][x])
                        last = edges[index][x]
                        last_index = index
                        points[idx][1] -= 1
                        break
                    else:
                        sequence.append(edges[index][x])
                        last = edges[index][x]
                        last_index = index
                        points[idx][1] -= 1
                        return sequence

    return sequence


def find_non_zero_occurence_point(points: list):
    """
   Looks for a point that has the number of occurences
   greater than 0.

    Args:
        points (list): The list of all unique points and their number of
        occurences.

    Returns:
        (int): The index of the point that was found.
    """
    index = -1
    for i in range(len(points)):
        if points[i][1] > 0:
            index = i
            break
    return index


def find_single_occurence_point(points: list):
    """
   Looks for a point that has the number of occurences
   is equal to 1.

    Args:
        points (list): The list of all unique points and their number of
        occurences.

    Returns:
        (int): The index of the point that was found.
    """
    index = -1
    for i in range(len(points)):
        if points[i][1] == 1:
            index = i
            break
    return index


def get_sequences_extended(edges):
    """
   Creates the list of all unique points and their number of
   occurences. After that, the list of sequences that use all
   edges is created.


    Args:
        edges (list): The list of all edges.

    Returns:
        list: the list of lists. It is the list of all sequences
        extracted based on the edges list.
    """
    points = get_points(edges)
    sequences = []
    checked = np.zeros(len(edges))
    while(True):
        index = find_single_occurence_point(points)
        if index == -1:
            min = len(points)
            for i in range(len(points)):
                if points[i][1] > 0 and points[i][1] < min and points[i][2] == 1:
                    min = points[i][1]
                    index = i
        if index != -1:
            sequence1 = one_way_append(edges, points, index, checked)
            sequences.append(sequence1)
        else:
            index = find_non_zero_occurence_point(points)
            if index != -1:
                sequence1 = one_way_append(edges, points, index, checked)
                sequences.append(sequence1)
            else:
                break
    return sequences
