import numpy as np
import cv2
import math
import random


def control_points(path_to_image: str):
    """#TODO

    Args:
        path_to_image (str): [description]

    Returns:
        [type]: [description]
    """
    img = cv2.imread(path_to_image)
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    contours = sorted(contours, key=lambda x: cv2.contourArea(x))[:-1]
    result = list()
    for cnt in contours:
        # compute the center of the contour
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        result.append((cX, cY))
    return result


def is_point_between(a, b, points):
    (x0, x1) = (a[0], b[0]) if a[0] < b[0] else (b[0], a[0])
    (y0, y1) = (a[1], b[1]) if a[1] < b[1] else (b[1], a[1])
    for point in points:
        if point[0] > x0 and point[0] < x1 and point[1] > y0 and point[1] < y1:
            return False
    return True


def points_distance(p1, p2):
    return math.sqrt(
        ((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2))


def line_coordinate(p1, p2):
    result = set()
    result.add(p1)
    for i in range(100):
        result.add((int(p1[0] + i / 100 * (p2[0] - p1[0])),
                    int(p1[1] + i / 100 * (p2[1] - p1[1]))))
    result.add(p2)
    return result


def is_point_in_shape(point, shape):
    if cv2.pointPolygonTest(shape, point, True) <= 0:
        return False
    return True


def degree_between_points(origin, p1, p2):
    vector_1 = [p1[0] - origin[0], p1[1] - origin[1]]
    vector_2 = [p2[0] - origin[0], p2[1] - origin[1]]

    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    return np.arccos(dot_product)


def degree_between_point_and_vector(p1, p2, vector_1):
    vector_2 = [p2[0] - p1[0], p2[1] - p1[1]]

    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    return np.arccos(dot_product)


def connected_points(points, path_to_skel, path_to_letter):
    image = cv2.imread(path_to_letter, cv2.IMREAD_COLOR)

    # for point in points:
    #     image = cv2.circle(image, point, radius=1,
    #                        color=(0, 0, 255), thickness=-1)

    # image = cv2.line(image, points[0], points[4],
    #                  color=(0, 0, 255), thickness=1)
    height, width, _ = image.shape
    factor = 2
    img2 = image
    img = image_resize(img2, width * factor, height * factor)
    img[:] = [255, 255, 255]
    img[int(height / 2):int(height / 2 + height),
        int(width / 2): int(width / 2 + width)] = image

    points_rescale = list()
    for i in range(len(points)):
        points_rescale.append((points[i][0] + int(width / 2),
                               points[i][1] + int(height / 2)))

    # cv2.imshow("t1", img)
    # cv2.waitKey()
    image = img

    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x))[:-1]

    lenght = len(points)
    biggest_cnt = contours[-1]
    contours = contours[:-1]
    result = set()
    for i in range(lenght - 1):
        point_a = points_rescale[i]

        for j in range(i, lenght):
            point_b = points_rescale[j]

            r = True
            for point in line_coordinate(point_a, point_b):
                if not is_point_in_shape(point, biggest_cnt):
                    r = False
                    break
                for cnt in contours:
                    if is_point_in_shape(point, cnt):
                        r = False
                        break
                if not r:
                    break
            if r:
                result.add((points[i], points[j]))
                # img2 = cv2.line(image, point_a, point_b,
                #                 color=(0, 0, 255), thickness=1)
    # cv2.imshow("t", img2)
    # cv2.waitKey()

    # for cnt in contours:
    #     cv2.drawContours(image, [cnt], 0, (0, 255, 0), 3)

    # height, width, _ = img2.shape
    # factor = 4
    # img2 = image_resize(img2, width * factor, height * factor)

    # cv2.imshow("t", img2)
    # cv2.waitKey()
    p = points[7]
    show_lines_for_point(p, result, path_to_letter)

    f = 6
    degree = 2 * np.pi / f
    len_before = len(result)
    for point in points:
        lines = list()
        for item in result:
            if item[0] == point:
                lines.append((item, points_distance(
                    item[0], item[1]), False))
            elif item[1] == point:
                lines.append(((item[1], item[0]), points_distance(
                    item[0], item[1]), True))
        for i in range(f):
            deg = degree * i
            vector = (math.sin(deg), math.cos(deg))
            lines_deg = [line for line in lines if degree_between_point_and_vector(
                line[0][0], line[0][1], vector) < degree]
            lenght = len(lines_deg)
            if point is p and lenght > 0:
                tmp = [lin[0] for lin in lines_deg]
                img2 = cv2.imread(path_to_letter, cv2.IMREAD_COLOR)
                color = (0, 255, 0)  # random_color()
                for line in tmp:
                    img2 = cv2.line(img2, line[0], line[1],
                                    color, thickness=1)

                height, width, _ = img2.shape
                img2 = cv2.line(img2, (height / 2, width / 2), (height / 2 + vector[0] * 5, width / 2 + vector[1] * 5),
                                (0, 255, 255), thickness=1)
                print(height, width)
                factor = 4
                img2 = image_resize(img2, width * factor, height * factor)

                cv2.imshow(str(lines), img2)
                cv2.waitKey()
            delete_set = set()
            if lenght > 1:
                for i in range(lenght - 1):
                    line_a = lines_deg[i]
                    for j in range(i, lenght):
                        line_b = lines_deg[j]
                        if line_a[1] > line_b[1]:
                            del_line = line_a
                        else:
                            del_line = line_b
                        if del_line[2]:
                            delete_set.add((del_line[0][1], del_line[0][0]))
                        else:
                            delete_set.add((del_line[0]))
                result.difference_update(delete_set)

    print(len_before, len(result))
    show_lines_for_point(p, result, path_to_letter)
    return result


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


def random_color():
    rgbl = [255, 0, 0]
    random.shuffle(rgbl)
    return tuple(rgbl)


def show_lines_for_point(point, connections, path_to_letter):
    lines = set()
    for item in connections:
        if item[0] == point or item[1] == point:
            lines.add(item)
    show_lines(lines, path_to_letter)


def show_lines(lines, path_to_letter):
    img2 = cv2.imread(path_to_letter, cv2.IMREAD_COLOR)
    color = (0, 255, 0)  # random_color()
    for line in lines:
        img2 = cv2.line(img2, line[0], line[1],
                        color, thickness=1)

    height, width, _ = img2.shape
    print(height, width)
    factor = 4
    img2 = image_resize(img2, width * factor, height * factor)
    cv2.imshow(str(lines), img2)
    cv2.waitKey()


if __name__ == '__main__':
    path_to_control_points = 'D:\\Git Repositories\\Handwriting-synthesis-with-the-help-of-machine-learning\\src\\graphical_interface\\letters_dataset\\A\\skel\\0_skel_control_points.png'
    path_to_skel = 'D:\\Git Repositories\\Handwriting-synthesis-with-the-help-of-machine-learning\\src\\graphical_interface\\letters_dataset\\A\\skel\\0_skel.png'
    path_to_letter = 'D:\\Git Repositories\\Handwriting-synthesis-with-the-help-of-machine-learning\\src\\graphical_interface\\letters_dataset\\A\\0.png'
    points = control_points(path_to_control_points)
    print(points)
    connections = connected_points(points, path_to_skel, path_to_letter)
    # print(connections)
    image = cv2.imread(path_to_letter, cv2.IMREAD_COLOR)
    # print(connections)
    # for point in points:
    #     lines = set()
    #     for item in connections:
    #         if item[0] == point or item[1] == point:
    #             lines.add(item)
    #     img2 = cv2.imread(path_to_letter, cv2.IMREAD_COLOR)
    #     print(point, lines)
    #     color = random_color()
    #     for line in lines:
    #         img2 = cv2.line(img2, line[0], line[1],
    #                         color, thickness=1)

    #     height, width, _ = img2.shape
    #     print(height, width)
    #     factor = 4
    #     img2 = image_resize(img2, width * factor, height * factor)

    #     cv2.imshow(str(point), img2)
    # cv2.waitKey()

    for line in connections:
        image = cv2.line(image, line[0], line[1],
                         color=(0, 0, 255), thickness=1)

    height, width, _ = image.shape
    factor = 4
    image = image_resize(image, width * factor, height * factor)

    cv2.imshow("result", image)
    cv2.waitKey()
