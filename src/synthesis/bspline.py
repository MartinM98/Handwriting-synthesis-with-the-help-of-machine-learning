# from src.file_handler.file_handler import get_absolute_path
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from src.file_handler.file_handler import get_absolute_path


def draw_bspline(points):
    """#TODO

    Args:
        points ([type]): [description]
    """
    x = points[:, 0]
    y = points[:, 1]

    # x=np.append(x,x[0])
    # y=np.append(y,y[0])

    tck, u = interpolate.splprep([x, y], k=2, s=1)
    u = np.linspace(0, 1, num=50, endpoint=True)
    out = interpolate.splev(u, tck)

    plt.figure()
    plt.plot(x, y, 'ro', out[0], out[1], 'b')
    plt.legend(['Points', 'Interpolated B-spline', 'True'], loc='best')
    plt.axis([min(x) - 1, max(x) + 1, min(y) - 1, max(y) + 1])
    plt.title('B-Spline interpolation')
    plt.show()


def save_bspline(points, path_to_save_file):
    """#TODO

    Args:
        points ([type]): [description]
    """
    x = points[:, 0]
    y = points[:, 1]

    plt.figure(1)
    draw_letter(x, y, plt)
    plt.savefig(path_to_save_file)
    plt.close(1)


def draw_letter(letter, plot=None, offset_x=0, offset_y=0, path_to_save_file=None):
    if plot is None:
        plot = plt
        plot.figure(1)
    min_x, min_y = 9999, 9999
    max_x, max_y = 0, 0
    for line in letter:
        if offset_x != 0 or offset_y != 0:
            line = [(point[0] + offset_x, point[1] + offset_y)
                    for point in line]
        line = np.array(line)
        x = line[:, 0]
        y = line[:, 1]

        if min(x) < min_x:
            min_x = min(x)
        if min(y) < min_y:
            min_y = min(y)
        if max(x) > max_x:
            max_x = max(x)
        if max(y) > max_y:
            max_y = max(y)

        tck, u = interpolate.splprep([x, y], k=2, s=1)
        u = np.linspace(0, 1, num=50, endpoint=True)
        out = interpolate.splev(u, tck)

        plot.plot(x, y, 'ro', out[0], out[1], 'b')
    if plot is None:
        plot.legend(['Points', 'Interpolated B-spline', 'True'], loc='best')
        plot.axis([min_x - 1, max_x + 1, min_y - 1, max_y + 1])
        plot.title('B-Spline interpolation')
        plot.show()
    if path_to_save_file is not None:
        plot.savefig(path_to_save_file)
        plot.close(1)  
    return min_x, max_x, min_y, max_y


def draw_word(letters):
    minimum_x, minimum_y = 9999, 9999
    maximum_x, maximum_y = 0, 0
    offset_x = 0
    plt.figure()
    for letter in letters:
        min_x, max_x, min_y, max_y = draw_letter(letter, plt, offset_x)

        if min_x < minimum_x:
            minimum_x = min_x
        if min_y < minimum_y:
            minimum_y = min_y
        if max_x > maximum_x:
            maximum_x = max_x
        if max_y > maximum_y:
            maximum_y = max_y
        offset_x = max_x

    plt.legend(['Points', 'Interpolated B-spline', 'True'], loc='best')
    plt.axis([minimum_x - 1, maximum_x + 1, minimum_y - 1, maximum_y + 1])
    plt.title('B-Spline interpolation')
    plt.show()


if __name__ == '__main__':
    letter_b = [[(10, -10), (11, -20), (12, -24), (13, -30), (14, -31), (15, -32), (16, -33), (21, -33), (24, -32), (25, -31),
                 (27, -30), (28, -29), (29, -27), (30, -22), (29, -20), (28, -19), (22, -19), (20, -20), (19, -21), (17, -22), (16, -23), (14, -24)]]
    moved_letter_b = list()
    for line in letter_b:
        line1 = list()
        for point in line:
            point1 = (point[0], point[1] + 20)
            line1.append(point1)
        moved_letter_b.append(line1)
    letter_x = [[(11, -11), (20, -22), (25, -28), (29, -34)],
                [(29, -11), (25, -18), (20, -24), (11, -34)]]
    moved_letter_x = list()
    for line in letter_x:
        line1 = list()
        for point in line:
            point1 = (point[0], point[1] + 20)
            line1.append(point1)
        moved_letter_x.append(line1)

    # points = draw_bspline(ctr)
    # save_bspline(ctr, get_absolute_path('./bsline.png'))
    letters = list()
    letters.append(letter_b)
    letters.append(letter_x)
    letters.append(letter_b)
    letters.append(moved_letter_x)
    letters.append(letter_b)
    letters.append(moved_letter_b)
    # letters.append(letter_b)
    # letters.append(moved_letter_b)
    # draw_word(letters)
    path_to_save = get_absolute_path('./bspline.png')
    draw_letter(letter_b, path_to_save_file=path_to_save)
