# std

# 3rd
from numpy.lib.function_base import interp
import pyglet
import pyglet.gl as gl
import pyglet.graphics as graphics

import numpy as np

# loc
#from .cell import Cell


class Grid(object):
    def __init__(self, window, first_player="X") -> None:
        self._window = window

        # make minimum border padding
        self._right_padding = (1.0 - 0.05) * window.width
        self._left_padding = 0.05 * window.width
        self._top_padding = (1.0 - 0.05) * window.height
        self._bottom_padding = 0.05 * window.height

        # Line properties
        self.LW = 5
        self.LC = tuple((0, 0, 0))

        # Player controller
        self._next_player = first_player

        # Data value
        self._Grid = np.full(shape=(3, 3), fill_value="", dtype=np.str)

    def __call__(self, x, y) -> None:
        intptx = int(x // (self._window.height / 3))
        intpty = int(y // (self._window.height / 3))

        if self.inside_padding(x, y):
            print(intptx, intpty)

    def inside_padding(self, x, y) -> bool:
        left = self._left_padding
        right = self._right_padding
        bottom = self._bottom_padding
        top = self._top_padding

        if left < x < right and bottom < y < top:
            return True
        else:
            return False

    def layout(self) -> None:
        padding = np.array(((self._left_padding, self._right_padding),
                            (self._bottom_padding, self._top_padding)))

        lines = np.array(
            ((1 / 3) * (padding[:, 1] - padding[:, 0]) + padding[:, 0],
             (2 / 3) * (padding[:, 1] - padding[:, 0]) + padding[:, 0]),
            dtype=np.uint16)

        # Set linewidth
        gl.glLineWidth(self.LW)

        for x, y in lines:
            # Draw horizontal lines
            graphics.draw(2, gl.GL_LINES,
                          ("v2f/static",
                           (self._left_padding, y, self._right_padding, y)),
                          ("c4B", (*self.LC, 255, *self.LC, 255)))

            # Draw vertical lines
            graphics.draw(2, gl.GL_LINES,
                          ("v2f/static",
                           (x, self._bottom_padding, x, self._top_padding)),
                          ("c4B", (*self.LC, 255, *self.LC, 255)))


window = pyglet.window.Window(500, 500, resizable=True)
gl.glClearColor(1.0, 1.0, 1.0, -1.0)
p = Grid(window)


@window.event
def on_draw():
    window.clear()

    p.layout()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == 1:
        p(x, y)


pyglet.app.run()
