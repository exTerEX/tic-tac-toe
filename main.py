""" Class for window creation and handling. """

import os
import numpy
import pyglet
import tkinter


def draw_grid(win: object, lw: int = 3, color=(0, 0, 0)) -> object:
    """ Function to draw the sudoku grid. """
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
    """"""
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
window.set_icon(*(pyglet.image.load("assets/icon/ico_16.png"),
                  pyglet.image.load("assets/icon/ico_32.png"),
                  pyglet.image.load("assets/icon/ico_64.png"),
                  pyglet.image.load("assets/icon/ico_128.png")))

# Grid centers
y_points = [(window.height * 0.95 - window.height * 0.15) * ratio
            for ratio in (0.25, 0.50, 0.75)]
x_points = [(window.width * 0.95 - window.width * 0.05) * i
            for i in (0.25, 0.50, 0.75)]


@window.event
def on_resize(width, height):
    """ Function to force correct window ratio to PyGlet. """
    pyglet.gl.glClearColor(1., 1., 1., -1)

    window.set_size(width, numpy.uint16(width * (6 / 5)))


@window.event
def on_draw():
    """ Graphical drawing function """
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

            print(numpy.rot90(Grid))

    # TODO: Implement victory condition.


@window.event
def on_mouse_release(x, y, button, modifiers):
    pass


@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    pass


@window.event
def on_mouse_motion(x, y, dx, dy):
    pass


@window.event
def on_mouse_enter(x, y):
    pass


@window.event
def on_mouse_leave(x, y):
    pass


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    pass


@window.event
def on_key_release(symbol, modifiers):
    pass


@window.event
def on_text(text):
    pass


@window.event
def on_text_motion(motion):
    pass


pyglet.app.run()
window.push_handlers(
    pyglet.window.event.WindowEventLogger(
        open(os.path.join("log/", "event.log"), "w")))
