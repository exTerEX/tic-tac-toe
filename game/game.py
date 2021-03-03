#!/usr/bin/env python3

from math import inf
from random import choice
import copy


class Game:
    def __init__(self):
        self._useradd_puzzle = [[0] * 3 for i in range(3)]

        self._ai_symbol = None
        self._player_symbol = None

        self._game_over_status = False

        self._winner = None

        self._count = 9

    @property
    def game_over_status(self):
        return self._game_over_status

    @property
    def winner(self):
        return self._winner

    def board(self, row, col):
        return self._useradd_puzzle[row][col]

    def player_symbol(self, symbol):
        self._player_symbol = symbol
        self._ai_symbol = -symbol

    def reset(self):
        self._useradd_puzzle = [[0] * 3 for i in range(3)]
        self._count = 9
        self._game_over_status = False

    def actions(self, board):
        possible = set()

        for index, row in enumerate(board):
            for jndex, col in enumerate(row):
                if col == 0:
                    possible.add((index, jndex))

        return possible

    def count(self, board):
        player = 0
        computer = 0

        for y_axis in board:
            for x_axis in y_axis:
                if x_axis == self._player_symbol:
                    player += 1
                elif x_axis == self._ai_symbol:
                    computer += 1

        if player <= computer:
            return self._player_symbol
        else:
            return self._ai_symbol

    def result(self, board, action):
        if len(action) != 2:
            raise Exception("incorrect action")

        if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
            raise Exception("incorrect action value")

        y, x = action[0], action[1]

        board_copy = copy.deepcopy(board)

        if board_copy[y][x] != 0:
            raise Exception("suggested action has already been taken")
        else:
            board_copy[y][x] = self.count(board)

        return board_copy

    def _win(self, board):
        for y in range(3):
            if (board[y][0] == board[y][1] == board[y][2]) and (board[y][0] != 0):
                return board[y][0]

            if (board[0][y] == board[1][y] == board[2][y]) and (board[0][y] != 0):
                return board[0][y]

        if (board[0][0] == board[1][1] == board[2][2]) or (
                board[0][2] == board[1][1] == board[2][0]) and board[1][1] != 0:
            return board[1][1]

        return None

    def terminal(self, board):
        if self._win(board) == self._player_symbol or self._win(board) == self._ai_symbol:
            return True
        elif 0 not in board[0] and 0 not in board[1] and 0 not in board[2]:
            return True
        else:
            return False

    def utility(self, board):
        if self._win(board) == self._player_symbol:
            return self._player_symbol
        elif self._win(board) == self._ai_symbol:
            return self._ai_symbol
        else:
            return 0

    def minimax(self, board):
        if self.terminal(board):
            return None

        if self.count(board) == self._player_symbol:
            score = -inf
            action_to_take = None

            for action in self.actions(board):
                min_val = self.minvalue(self.result(board, action))

                if min_val > score:
                    score = min_val
                    action_to_take = action

            return action_to_take

        elif self.count(board) == self._ai_symbol:
            score = inf
            action_to_take = None

            for action in self.actions(board):
                max_val = self.maxvalue(self.result(board, action))

                if max_val < score:
                    score = max_val
                    action_to_take = action

            return action_to_take

    def minvalue(self, board):
        if self.terminal(board):
            return self.utility(board)

        max_value = inf
        for action in self.actions(board):
            max_value = min(max_value, self.maxvalue(self.result(board, action)))

        return max_value

    def maxvalue(self, board):
        if self.terminal(board):
            return self.utility(board)

        min_val = -inf
        for action in self.actions(board):
            min_val = max(min_val, self.minvalue(self.result(board, action)))

        return min_val

    def check_win(self):
        if self._win(self._useradd_puzzle) == self._player_symbol:
            self._game_over_status = True
            self._winner = self._player_symbol
        elif self._win(self._useradd_puzzle) == self._ai_symbol:
            self._game_over_status = True
            self._winner = self._ai_symbol
        elif self._count == 0:
            self._game_over_status = True

        return

    def ai(self):
        self.check_win()
        if self._count == 0 or self._game_over_status:
            return

        row, col = 0, 0
        if self._count == 9:
            row = choice([0, 1, 2])
            col = choice([0, 1, 2])
        else:
            move = self.minimax(self._useradd_puzzle)
            row, col = move[0], move[1]

        self._useradd_puzzle[row][col] = self._ai_symbol
        self._count -= 1

        self.check_win()

    def human(self, row, col):
        self.check_win()
        if self._count == 0 or self._game_over_status:
            return

        if self._useradd_puzzle[row][col] == 0:
            self._useradd_puzzle[row][col] = self._player_symbol
            self._count -= 1
            return True

        self.check_win()
