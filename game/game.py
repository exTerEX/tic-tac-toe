""" Class for window creation and handling. """

import json
import numpy as np
import pyglet
import pyglet.gl as gl
import pyglet.resource as resource
import pyglet.graphics as graphics

# Global constant variables
BACKGROUND_COLOR: tuple = tuple((0.95, 0.98, 0.94))


class Grid(object):
    def __init__(self, window, first_player="X") -> None:
        self._window = window

        # make minimum border padding
        self._right_padding = (1.0 - 0.05) * window.width
        self._left_padding = 0.05 * window.width
        self._top_padding = (1.0 - 0.05) * window.height
        self._bottom_padding = 0.05 * window.height

        # Line properties
        self.lw = 5
        self.lc = tuple((0, 0, 0))

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
        gl.glLineWidth(self.lw)

        for x, y in lines:
            # Draw horizontal lines
            graphics.draw(2, gl.GL_LINES,
                          ("v2f/static",
                           (self._left_padding, y, self._right_padding, y)),
                          ("c4B", (*self.lc, 255, *self.lc, 255)))

            # Draw vertical lines
            graphics.draw(2, gl.GL_LINES,
                          ("v2f/static",
                           (x, self._bottom_padding, x, self._top_padding)),
                          ("c4B", (*self.lc, 255, *self.lc, 255)))


# Define window and global window properties
window = pyglet.window.Window(500,
                              600,
                              "Tic-Tac-Toe",
                              resizable=True,
                              visible=False)
game = Grid(window)

# Set resource search path and reindex
resource.path = json.load(open("tic-tac-toe/resources/source.json"))
resource.reindex()

# Set icons
window.set_icon(resource.image("3XT-016.png"), resource.image("3XT-032.png"),
                resource.image("3XT-064.png"), resource.image("3XT-128.png"))

# Set background
gl.glClearColor(*BACKGROUND_COLOR, -1.0)

# Make window visible
window.set_visible()


@window.event
def on_draw():
    window.clear()
    game.layout()


@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(0, width, 0, height, -1, 1)
    gl.glMatrixMode(gl.GL_MODELVIEW)


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == 1:
        game(x, y)


if __name__ == '__main__':
    pyglet.app.run()

#
#
"""class Main(pyglet.window.Window):
    def __init__(self, *args, **kwargs) -> None:
        super(Main, self).__init__(*args, **kwargs)
        gl.glClearColor(*BACKGROUND_COLOR, -1.0)  # Background color

        # Set minimum window size
        self.set_minimum_size(500, 600)

    def on_draw(self):
        self.clear()

    def on_resize(self, width, height):
        gl.glViewport(0, 0, width, height)


if __name__ == '__main__':
    window = Main(500, 600, "My Pyglet Window", resizable=True)
    pyglet.app.run()"""
"""
def draw_grid(win: object, lw: int = 3, color=(0, 0, 0)) -> object:
    index = 1

    for x_pos, y_pos in list(
            zip(numpy.linspace(0, win.width, 4),
                numpy.linspace(0, win.height * 0.9, 4)))[1:-1]:
        if index % 3 == 0:
            pyglet.gl.glLineWidth(lw + 3)
        else:
            pyglet.gl.glLineWidth(lw)
        pyglet.graphics.draw(
            2, pyglet.gl.GL_LINES,
            ("v2f/static",
             (win.width * 0.05, y_pos + win.height * 0.1,
              win.width - win.width * 0.05, y_pos + win.height * 0.1)),
            ("c4B", (*color, 255, *color, 255)))

        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                             ("v2f/static",
                              (x_pos, win.height * 0.1 + win.height * 0.05,
                               x_pos, win.height - win.height * 0.05)),
                             ("c4B", (*color, 255, *color, 255)))
        index += 1


# TODO: MAKE FUCKING LOGICAL WITHOUT USE OF CONSTANTS...
def draw_char(win: object, data: numpy.array):
    """ """
    for row in range(0, 3):
        for col in range(0, 3):
            if numpy.rot90(data)[row][col] != 0:
                _x = win.width * 0.05 + win.width * 0.9 * [
                    1 / 7, 1 / 2, 6 / 7
                ][col]
                _y = win.height * 0.05 + win.height * 0.85 * [
                    1 / 3.75, 2.25 / 3.75, 3.50 / 3.75
                ][2 - row]
                if numpy.rot90(data)[row][col] == 1:
                    pyglet.text.Label("X",
                                      x=_x,
                                      y=_y,
                                      font_size=96,
                                      color=(0, 0, 0, -1),
                                      anchor_x="center",
                                      anchor_y="center").draw()
                else:
                    pyglet.text.Label("O",
                                      x=_x,
                                      y=_y,
                                      font_size=96,
                                      color=(0, 0, 0, -1),
                                      anchor_x="center",
                                      anchor_y="center").draw()
            else:
                continue


##### Global settings

# Values in grid
Grid = numpy.zeros((3, 3), dtype=numpy.int8)
count = 1

# These settings are only true for initiation
HEIGHT = numpy.uint16(tkinter.Tk().winfo_screenheight() * (1 / 2))
WIDTH = numpy.uint16(HEIGHT * (5 / 6))

# Load custom font(s)
pyglet.font.add_file("assets/font/cooper-black.ttf")

window = pyglet.window.Window(width=WIDTH,
                              height=HEIGHT,
                              resizable=True,
                              caption="Tic-Tac-Toe",
                              style=pyglet.window.Window.WINDOW_STYLE_DEFAULT)

# Sets the background color
pyglet.gl.glClearColor(1., 1., 1., -1)

# Sets the window icon
window.set_icon(*(pyglet.resource.image("assets/icon/ico_16.png"),
                  pyglet.resource.image("assets/icon/ico_32.png"),
                  pyglet.resource.image("assets/icon/ico_64.png"),
                  pyglet.resource.image("assets/icon/ico_128.png")))

# Grid centers
y_points = [(window.height * 0.95 - window.height * 0.15) * ratio
            for ratio in (0.25, 0.50, 0.75)]
x_points = [(window.width * 0.95 - window.width * 0.05) * i
            for i in (0.25, 0.50, 0.75)]


@window.event
def on_resize(width, height):
    pyglet.gl.glClearColor(1., 1., 1., -1)

    window.set_size(width, numpy.uint16(width * (6 / 5)))


@window.event
def on_draw():
    pyglet.gl.glClearColor(1., 1., 1., -1)

    window.clear()

    pyglet.gl.glLineWidth(5)
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                         ("v2f/static",
                          (window.width * 0.05, window.height * 0.1,
                           window.width * 0.95, window.height * 0.1)),
                         ("c3B", (0, 0, 0, 0, 0, 0)))

    draw_grid(window)
    draw_char(window, Grid)


@window.event
def on_mouse_press(x, y, button, modifiers):
    global count

    xpint = int(x // (window.width / 3))
    ypint = int(y // (window.height / 3))

    if window.width * 0.05 < x < window.width * 0.95 and window.height * 0.15 < y < window.height * 0.95:
        if Grid[xpint][ypint] == 0:
            if count % 2 == 0:
                Grid[xpint][ypint] = 1
            else:
                Grid[xpint][ypint] = -1
            count += 1
            draw_char(window, Grid)

            # Debugging
            print(numpy.rot90(Grid))

    # TODO: Implement better victory condition check.
    for row in Grid:
        if (row[0] == row[1] == row[2]) and (row[0] != 0 or row[1] or row[2]):
            print(f"Player {row[0]} won!")

    for row in numpy.rot90(Grid):
        if (row[0] == row[1] == row[2]) and (row[0] != 0 or row[1] or row[2]):
            print(f"Player {row[0]} won!")

    if (Grid[0][0] == Grid[1][1] == Grid[2][2]) and (Grid[0][0] != 0
                                                     or Grid[1][1] != 0
                                                     or Grid[2][2] != 0):
        print(f"Player {Grid[0][0]} won!")

    if (Grid[0][2] == Grid[1][1] == Grid[2][0]) and (Grid[0][2] != 0
                                                     or Grid[1][1] != 0
                                                     or Grid[0][2] != 0):
        print(f"Player {Grid[0][2]} won!")


pyglet.app.run()

logpath = "log/"
if not os.path.exists(logpath):
    os.mkdir(logpath)

window.push_handlers(
    pyglet.window.event.WindowEventLogger(
        open(os.path.join(logpath, "event.log"), "w")))
"""
