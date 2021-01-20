#!/usr/bin/env python3

from math import inf
from random import choice


class Game:
    def __init__(self, grid, mode="normal"):
        self._useradd_puzzle = [[0] * grid for i in range(grid)]

        self._grid = grid

        self._ai_symbol = None
        self._player_symbol = None

        self._game_over_status = False
        self._mode = mode

        self._winner = None

        self._count = 9

    def player_symbol(self, symbol):
        self._player_symbol = symbol
        self._ai_symbol = -symbol

    def reset(self):
        self._useradd_puzzle = [[0] * self._grid for i in range(self._grid)]
        self._count = 9

    @property
    def game_over_status(self):
        return self._game_over_status

    def check_win(self):
        if self._wins(self._player_symbol):
            self._game_over_status = True
            self._winner = self._player_symbol
        elif self._wins(self._ai_symbol):
            self._game_over_status = True
            self._winner = self._ai_symbol
        elif self._count == 0:
            self._game_over_status = True
        return

    @property
    def winner(self):
        return self._winner

    def _wins(self, player):
        if self._mode == "normal":
            board = self._useradd_puzzle
            win = [
                [board[0][0], board[0][1], board[0][2]],
                [board[1][0], board[1][1], board[1][2]],
                [board[2][0], board[2][1], board[2][2]],
                [board[0][0], board[1][0], board[2][0]],
                [board[0][1], board[1][1], board[2][1]],
                [board[0][2], board[1][2], board[2][2]],
                [board[0][0], board[1][1], board[2][2]],
                [board[2][0], board[1][1], board[0][2]]
            ]

            if [player, player, player] * 3 in win:
                return True
            else:
                return False
        elif self._mode == "super":
            return "Super model isn't implemented"

    def _empty(self):
        cells = []

        for x, row in enumerate(self._useradd_puzzle):
            for y, col in enumerate(row):
                if col == 0:
                    cells.append([x, y])

        return cells

    def minimax(self, depth=None, player=None):
        if depth is None:
            depth = self._count

        if player is None:
            player = self._ai_symbol

        best = [player, player, inf * player]

        score = 0
        if depth == 0 or self._game_over_status:
            if self._wins(self._ai_symbol):
                score = self._ai_symbol
            elif self._wins(self._player_symbol):
                score = self._player_symbol
            else:
                score = 0

            return [-1, -1, score]

        for cell in self._empty():
            row, col = cell[0], cell[1]
            self._useradd_puzzle[row][col] = self._ai_symbol
            score = self.minimax(depth=depth - 1, player=player)
            self._useradd_puzzle[row][col] = 0
            score[0], score[1] = row, col

            if player == self._ai_symbol:
                if score[2] > best[2]:
                    best = score
            else:
                if score[2] < best[2]:
                    best = score

            return best

    # FIXME: Some error when player start in left lower and middle corner stopping AI from working
    def ai(self):
        if self._count == 0 or self._game_over_status:
            return

        if self._mode == "normal":
            if self._count == 9:
                row = choice([0, 1, 2])
                col = choice([0, 1, 2])
            else:
                move = self.minimax()
                row, col = move[0], move[1]

            self._useradd_puzzle[row][col] = self._ai_symbol
            self._count -= 1
            print(self._count)
            print(self._useradd_puzzle)
        elif self._mode == "super":
            print("Not implemented")

        print()

    def human(self, row, col):
        if self._count == 0 or self._game_over_status:
            return

        if self._useradd_puzzle[row][col] == 0:
            self._useradd_puzzle[row][col] = self._player_symbol
            self._count -= 1
            return True
        else:
            return False
