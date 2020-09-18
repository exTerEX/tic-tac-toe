# // TODO: Make inherit GUI class to draw in window.
class Cell(object):
    def __init__(self, value: int, in_row: int, in_col: int) -> None:
        self._value = value
        self._in_row = in_row
        self._in_col = in_col
