# model/board.py
from config import GRID_SIZE


class Board:
    def __init__(self, size: int = GRID_SIZE):
        self.size = size
        self.data = self._make(size)

    def _make(self, size):
        board = []
        for _ in range(size):
            row = []
            for _ in range(size):
                row.append(0)
            board.append(row)
        return board

    def reset(self):
        self.data = self._make(self.size)

    def get(self, row, col):
        return self.data[row][col]

    def set(self, row, col, value):
        self.data[row][col] = value

    def is_empty(self, row, col):
        return self.data[row][col] == 0

    def is_full(self):
        for row in self.data:
            for cell in row:
                if cell == 0:
                    return False
        return True