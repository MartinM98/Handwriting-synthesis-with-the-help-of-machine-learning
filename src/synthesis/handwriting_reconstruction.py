from src.image_processing.skeletonize import skeletonize_image
import cv2
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from src.file_handler.file_handler import get_absolute_path
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import copy


def generate_bsplain(x: list, y: list):
    """
    Generate B splain for input points.

    Args:
        x (int): List of x valuses.
        y (int): List of y valuses.

    Returns:
        [list]: Gerenrated B splain.
    """
    tck, u = interpolate.splprep([x, y], k=2, s=1)
    u = np.linspace(0, 1, num=50, endpoint=True)
    return interpolate.splev(u, tck)


def generate_bsplain_fig(letter: list = None, plot: plt = None, offset_x: int = 0, offset_y: int = 0, path_to_save_file: str = None, image_size: tuple = None, show_points_flag: bool = False):
    """
    Generate B splain for input letter.

    Args:
        letter (list): List of lines (list of points) for which the B splain is computed and printed.
        plot (plt, optional): If provided then the new figure is the part of plot. Defaults to None.
        offset_x (int, optional): Offset in first points cooridante. Defaults to 0.
        offset_y (int, optional): Offset in second points cooridante. Defaults to 0.
        path_to_save_file (str, optional): If the path is provided then the image is saved in the location. Defaults to None.
        image_size (tuple, optional): If provided the output image is in the size. Defaults to None.
        show_points_flag (bool, optional): If true show points on image.  Defaults to False.

    Returns:
        fig : New figure with the B splain.
    """
    letter = letter if letter else []
    fig = None
    if plot is None:
        plot = plt
    letter = copy.deepcopy(letter)
    if image_size is not None:
        fig = plot.figure(1, figsize=(
            image_size[0] / 100, image_size[1] / 100))
    else:
        fig = plot.figure(1)
    for line in letter:
        if offset_x != 0 or offset_y != 0:
            line = [(point[0] + offset_x, point[1] + offset_y)
                    for point in line]
        line_length = len(line)
        if line_length > 2:
            line = np.array(line)
            x = line[:, 0]
            y = line[:, 1]

            out = generate_bsplain(x, y)

            if show_points_flag:
                plot.plot(x, y, 'ro', out[0], out[1], 'b')
            else:
                plot.plot(out[0], out[1], 'black')
        elif line_length == 2:
            plot.plot(line[0], line[1], 'black')
        elif line_length == 1:
            plot.plot(line[0][0], line[0][1], 'o', color='black')
    return fig


def draw_letter(letter: list = None, offset_x: int = 0, offset_y: int = 0, path_to_save_file: str = None, image_size: tuple = None, show_points_flag: bool = False, skeleton_flag: bool = False, show_flag: bool = True):
    """
    Create image with input letter, using the B spline the imitation of is made. Function has many parameters to define all imporatant features.

    Args:
        letter (list): List of lines (list of points) for which the B splain is computed and printed.
        offset_x (int, optional): Offset in first points cooridante. Defaults to 0.
        offset_y (int, optional): Offset in second points cooridante. Defaults to 0.
        path_to_save_file (str, optional): If the path is provided then the image is saved in the location. Defaults to None.
        image_size (tuple, optional): If provided the output image is in the size. Defaults to None.
        show_points_flag (bool, optional): If true then show points on image.  Defaults to False.
        skeleton_flag (bool, optional): If true then generate skeleton.  Defaults to False.
        show_flag (bool, optional): If true then show plot.  Defaults to False.
    Returns:
        image (image): Image with the created letter.
    """
    letter = letter if letter else []
    fig = None
    plot = plt
    letter = copy.deepcopy(letter)
    fig = generate_bsplain_fig(letter, plot, offset_x, offset_y,
                               path_to_save_file, image_size, show_points_flag)
    plot.axis('off')
    if path_to_save_file is None and show_flag:
        plot.show()
    canvas = FigureCanvas(fig)
    canvas.draw()
    width, height = fig.get_size_inches() * fig.get_dpi()
    image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(int(height), int(width), 3)
    plot.close()
    if skeleton_flag:
        image = skeletonize_image(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    if path_to_save_file is not None:
        cv2.imwrite(path_to_save_file, image)

    return image


def test():
    """
    Testing function.
    """
    letter_b = [[(10, -10), (11, -20), (12, -24), (13, -30), (14, -31), (15, -32), (16, -33), (21, -33), (24, -32), (25, -31),
                 (27, -30), (28, -29), (29, -27), (30, -22), (29, -20), (28, -19), (22, -19), (20, -20), (19, -21), (17, -22), (16, -23), (14, -24)]]
    letter_x = [[(11, -11), (20, -22), (25, -28), (29, -34)],
                [(29, -11), (25, -18), (20, -24), (11, -34)]]
    path_to_save = get_absolute_path('./bspline.png')
    draw_letter(letter_x, show_points_flag=True, skeleton_flag=False,
                path_to_save_file=path_to_save)
    draw_letter(letter_b, path_to_save_file=path_to_save)


if __name__ == '__main__':
    test()
