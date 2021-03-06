#!/usr/bin/env python3

from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

import random

# pyright: reportMissingImports=false
from game import Game


class Interface(Frame):
    def __init__(self, parent, side=150, margin=20):
        Frame.__init__(self, parent)

        self.parent = parent

        self.game = Game()

        self._side = side
        self._margin = margin
        self._height = margin * 2 + side * 3
        self._width = margin * 2 + side * 3

        self._player_turn = None
        self._player_symbol = None

        self.init()

    def init(self):
        self.parent.title("Tik-Tac-Toe")
        self.parent.wm_iconbitmap("game/resources/logo/tic-tac-toe-icon.ico")

        self.pack(fill=BOTH)
        self.canvas = Canvas(self, width=self._width, height=self._height)
        self.canvas.pack(fill=BOTH, side=TOP)

        clear_button = Button(self, text="Clear answers", command=self._clear_answers)
        clear_button.pack(fill=BOTH, side=BOTTOM)

        self.player_properties()

        self._draw_grid()

        if not self._player_turn:
            self.game.ai()
            self._player_turn = True

        self._draw_puzzle()

        self.canvas.bind("<Button-1>", self._cell_clicked)

    def player_properties(self):
        self._player_turn = random.choice([True, False])
        self._player_symbol = random.choices([+1, -1])[0]

        self.game.player_symbol(self._player_symbol)

    def _draw_grid(self):
        margin = self._margin
        side = self._side
        height = self._height
        width = self._width

        for index in range(3 + 1):
            color = "black" if index % 3 == 0 else "gray"

            # Vertical
            self.canvas.create_line(
                margin + index * side,
                margin,
                margin + index * side,
                height - margin,
                fill=color)

            # Horizontal
            self.canvas.create_line(
                margin,
                margin + index * side,
                width - margin,
                margin + index * side,
                fill=color)

    def _draw_puzzle(self):
        self.canvas.delete("checks")

        margin = self._margin
        side = self._side

        for index in range(3):
            for jndex in range(3):
                answer = self.game.board(index, jndex)

                if answer != 0:
                    color = "black"
                    text = "O"
                    if answer == 1:
                        color = "black"
                        text = "X"

                    self.canvas.create_text(
                        margin + jndex * side + side / 2,
                        margin + index * side + side / 2,
                        text=text,
                        tags="checks",
                        fill=color,
                        font=("Arial", int(0.85 * self._side)))

        if self.game.game_over_status:
            self._draw_victory()

    def _draw_victory(self):
        winner = self.game.winner

        text = ""
        if winner == self._player_symbol:
            text = "You win!"
        elif winner == -1 * self._player_symbol:
            text = "AI win!"
        elif winner is None:
            text = "Draw!"

        height = self._height
        width = self._width

        self.canvas.create_oval(
            int(width * 0.2),
            int(height * 0.2),
            int(width * 0.8),
            int(height * 0.8),
            tags="victory",
            fill="dark orange",
            outline="orange")

        self.canvas.create_text(
            int(width * 0.5),
            int(height * 0.5),
            text=text,
            tags="victory",
            fill="white",
            font=("Arial", 32))

    def _cell_clicked(self, event):
        if self.game.game_over_status:
            self._draw_victory()
            return

        margin = self._margin
        side = self._side

        x_pos, y_pos = event.x, event.y
        if (margin < x_pos < self._width - margin and margin < y_pos < self._height - margin):
            self.canvas.focus_set()

            row, col = int((y_pos - margin) / side), int((x_pos - margin) / side)

            allowed = self.game.human(row, col)
            if allowed:
                self.game.ai()

        self._draw_puzzle()

    def _clear_answers(self):
        self.canvas.delete("victory", "checks")
        self.game.reset()
        self.player_properties()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


if __name__ == "__main__":
    root = Tk()

    ui = Interface(root)

    root.geometry(f"{ui.width}x{ui.height + 40}")
    root.mainloop()
