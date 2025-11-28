# rules/check_winner.py
from typing import Optional, Sequence


def _check_line(line: Sequence[int], win_length: int) -> int | None:
    """Check a single 1D line for a winner with given win length.

    Returns:
        1  if player X wins
        -1 if player O wins
        None if no winner in this line
    """
    size = len(line)
    if win_length > size:
        return None

    start = 0
    while start <= size - win_length:
        segment = line[start : start + win_length]
        s = sum(segment)
        if s == win_length:
            return 1
        if s == -win_length:
            return -1
        start += 1

    return None


def check_winner(board, win_length: int | None = None) -> Optional[int]:
    """Check winner for a square board.

    Args:
        board: 2D list-like structure with values -1, 0, 1.
        win_length: how many in a row are needed to win.
            If None, uses full board size (classic tic-tac-toe).

    Returns:
        1   if player X wins
        -1  if player O wins
        0   if draw
        None if game is still in progress
    """
    size = len(board)
    if size == 0:
        return None

    target = win_length or size
    if target < 1:
        return None

    # horizontal
    for row in board:
        res = _check_line(row, target)
        if res is not None:
            return res

    # vertical
    for col in range(size):
        column = [board[row][col] for row in range(size)]
        res = _check_line(column, target)
        if res is not None:
            return res

    # main diagonals (top-left to bottom-right)
    for start_row in range(size - target + 1):
        diag = [board[start_row + k][k] for k in range(size - start_row)]
        res = _check_line(diag, target)
        if res is not None:
            return res

    for start_col in range(1, size - target + 1):
        diag = [board[k][start_col + k] for k in range(size - start_col)]
        res = _check_line(diag, target)
        if res is not None:
            return res

    # anti-diagonals (top-right to bottom-left)
    for start_row in range(size - target + 1):
        diag = [board[start_row + k][size - 1 - k] for k in range(size - start_row)]
        res = _check_line(diag, target)
        if res is not None:
            return res

    for start_col in range(size - 2, target - 2, -1):
        diag = [board[k][start_col - k] for k in range(start_col + 1)]
        res = _check_line(diag, target)
        if res is not None:
            return res

    # draw?
    for row in board:
        if 0 in row:
            return None

    return 0