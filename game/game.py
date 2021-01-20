#!/usr/bin/env python3


class Game:
    def __init__(self, grid):
        self._useradd_puzzle = [[0] * grid for i in range(grid)]

        self._grid = grid

        self._game_over_status = False

    @property
    def game_over_status(self):
        return self._game_over_status

    def check_win(self):
        pass

        self._game_over_status = True

        return True
