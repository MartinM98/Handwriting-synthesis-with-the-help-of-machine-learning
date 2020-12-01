from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import cv2

fig = Figure()
canvas = FigureCanvas(fig)
ax = fig.gca()

ax.text(0.0, 0.0, "Test", fontsize=45)
ax.axis('off')

canvas.draw()       # draw the canvas, cache the renderer
width, height = fig.get_size_inches() * fig.get_dpi()
image = np.fromstring(canvas.tostring_rgb(), dtype='uint8')
image = image.reshape(int(height), int(width), 3)
cv2.imshow("test", image)
cv2.waitKey()
