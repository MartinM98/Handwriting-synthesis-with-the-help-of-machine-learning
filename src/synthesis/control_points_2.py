from src.synthesis.bspline import draw_bspline
import cv2
from matplotlib import pyplot as plt
import numpy as np
import math


def neighbour_pixel(p1, p2):
    if abs(p1[0] - p2[0]) < 2 and abs(p1[1] - p2[1]) < 2:
        return True
    return False


def points_distance(p1, p2):
    return math.sqrt(
        ((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2))


def skel_to_graph(path_to_skel):
    image = cv2.imread(path_to_skel)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Set threshold level
    threshold_level = 50
    # Find coordinates of all pixels below threshold
    vertices = np.column_stack(np.where(gray < threshold_level))
    vertices = [(v[0], v[1]) for v in vertices]

    edges = set()
    for v in vertices:
        for ver in vertices:
            if ver is not v and neighbour_pixel(v, ver) and not (ver, v) in edges:
                edges.add((v, ver))

    image[:] = (255, 255, 255)
    for v in vertices:
        image[v[0], v[1]] = (0, 0, 0)

    return vertices, edges


def draw_graph(vertices, edges):
    # x axis value list.
    x_number_list = [v[0] for v in vertices]

    # y axis value list.
    y_number_list = [v[1] for v in vertices]

    plt.axis([min(x_number_list) - 1, max(x_number_list) + 1,
              min(y_number_list) - 1, max(y_number_list) + 1])

    # Draw point based on above x, y axis values.
    plt.scatter(x_number_list, y_number_list, s=10)

    for e in edges:
        x = list()
        y = list()
        x.append(e[0][0])
        x.append(e[1][0])
        y.append(e[0][1])
        y.append(e[1][1])
        plt.plot(x, y)

    # Set chart title.
    plt.title("Extract Number Root ")

    # Set x, y label text.
    plt.xlabel("Number")
    plt.ylabel("Extract Root of Number")
    plt.show()


def point_in_area(p, x_min, x_max, y_min, y_max):
    if p[0] >= x_min and p[0] <= x_max and p[1] >= y_min and p[1] <= y_max:
        return True
    return False


def find_neighbours(vertex, edges):
    result = set()
    for e in edges:
        if e[0] == vertex:
            result.add(e[1])
        elif e[1] == vertex:
            result.add(e[0])
    return result


def remove_edge(edges, v1, v2):
    edges.discard((v1, v2))
    edges.discard((v2, v1))


def find_cycles(vertices, edges):
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


def remove_cycles(vertices, edges):
    cycles = find_cycles(vertices, edges)
    for cycle in cycles:
        for c1 in cycle:
            for c2 in cycle:
                if c1 is not c2 and points_distance(c1, c2) > 1:
                    remove_edge(edges, c1, c2)

    return vertices, edges


def sort_neighbours(neighbours):
    neighbours = list(neighbours)
    return sorted(neighbours, key=lambda element: (element[0], element[1]))


def inster_to_sorted(ver):
    pass


def sort_edges(vertices, edges):
    sorted = list()
    for j in range(len(vertices)):
        if not vertices[j] in sorted:
            sorted.append(vertices[j])
        neighbours = find_neighbours(vertices[j], edges)
        i = sorted.index(vertices[j])
        length = len(neighbours)
        if length == 1:
            n = sort_neighbours(neighbours)
            if not n[0] in sorted:
                sorted.insert(i + 1, n[0])
        if length == 2:
            n = sort_neighbours(neighbours)
            if not n[0] in sorted:
                sorted.insert(i, n[0])
            if not n[1] in sorted:
                sorted.insert(i + 2, n[1])
    return sorted


def compate_points(p1, p2):
    if p1[0] == p2[0] and p1[1] == p2[1]:
        return True
    return False


def martin(edges):
    pairs = list(edges)
    print(edges)
    sequence = []
    sequence.append(pairs[0][0])
    sequence.append(pairs[0][1])
    last = pairs[0][1]
    last_index = 0
    for i in range(0, len(pairs)):
        for index in range(1, len(pairs)):
            if index != last_index:
                first = compate_points(pairs[index][0], last)
                second = compate_points(pairs[index][1], last)
                if first or second:
                    if first:
                        sequence.append(pairs[index][1])
                        last = pairs[index][1]
                    if second:
                        sequence.append(pairs[index][0])
                        last = pairs[index][0]
                    last_index = index
                    break
    return sequence


if __name__ == '__main__':
    path_to_skel = 'D:\\Git Repositories\\Handwriting-synthesis-with-the-help-of-machine-learning\\src\\graphical_interface\\letters_dataset\\A\\skel\\0_skel.png'
    path_to_line = 'C:\\Users\\Patryk\\Desktop\\line.png'
    path_to_martin = 'C: \Users\Patryk\Downloads\'
    vertices, edges = skel_to_graph(path_to_skel)
    draw_graph(vertices, edges)
    remove_cycles(vertices, edges)

    # sorted = sort_edges(vertices, edges)
    draw_graph(vertices, edges)
    # draw_bspline(np.array(sorted))
    # result = martin(edges)
    # print(result)
    # draw_bspline(np.array(result))
