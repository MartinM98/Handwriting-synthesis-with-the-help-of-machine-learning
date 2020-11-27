import numpy as np
from scipy import interpolate

import matplotlib.pyplot as plt


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


if __name__ == '__main__':
    ctr = np.array([(10, -10), (11, -20), (12, -24), (13, -30), (14, -31), (15, -32), (16, -33), (21, -33), (24, -32), (25, -31),
                    (27, -30), (28, -29), (29, -27), (30, -22), (29, -20), (28, -19), (22, -19), (20, -20), (19, -21), (17, -22), (16, -23), (14, -24)])
    ctr
    points = draw_bspline(ctr)
